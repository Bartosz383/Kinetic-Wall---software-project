import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import serial
import time

def resize_and_convert_to_gray(input_paths, output_folder, motor_speed, selected_port):
    if not input_paths:
        messagebox.showerror("Błąd", "Nie wybrano żadnych plików wejściowych.")
        return

    for input_path in input_paths:
        try:
            original_image = cv2.imread(input_path)
            if original_image is None:
                messagebox.showerror("Błąd", "Nie można wczytać pliku: {}".format(input_path))
                continue

            resized_image_32x16 = cv2.resize(original_image, (32, 16))
            gray_image_32x16 = cv2.cvtColor(resized_image_32x16, cv2.COLOR_BGR2GRAY)
            filename = input_path.split("/")[-1]

            cv2.imwrite(output_folder + "/{}_32x16.jpg".format(filename), gray_image_32x16)

            dane = gray_image_32x16.tolist()  # Konwersja macierzy numpy na listę

            # Stworzenie segmentów i zapisanie ich do pliku
            segment_vectors = [
                create_segment_vector(dane, i * 4, (i + 1) * 4, j * 4, (j + 1) * 4, f"segment_{i * 8 + j}")
                for i in range(4)
                for j in range(8)
            ]

            motor_speed_value = max(0, min(int(motor_speed.get()) if motor_speed.get() else 150, 255))  # Ograniczenie prędkości do przedziału od 0 do 255

            save_frames(segment_vectors, motor_speed_value, output_folder, filename)
            send_frames(segment_vectors, motor_speed_value, selected_port.get())
            # save_segment_vectors(segment_vectors, output_folder, filename)

        except Exception as e:
            messagebox.showerror("Błąd", "Wystąpił błąd podczas przetwarzania pliku: {}\n{}".format(input_path, str(e)))
    messagebox.showinfo("Informacja", "Konwersja zakończona pomyślnie.")


def calculate_xor_checksum(bit2, bit3, bit4, bit5):
    return bit2 ^ bit3 ^ bit4 ^ bit5

def prepare_frame(bit2, bit3, bit4, bit5):
    checksum = calculate_xor_checksum(bit2, bit3, bit4, bit5)
    frame = bytearray([
        0x55,  # Start
        bit2,  # segment address
        bit3,  # motor address (wartości od 0 do 15, iterowane w kółko)
        bit4,  # requested motor angle; value (segment)
        bit5,  # motor speed
        checksum,  # XOR checksum
        0xAA  # Stop
    ])
    return frame


def send_frames(segment_vectors, motor_speed, selected_port):
    # Serial port configuration
    port = selected_port  # Change this to the selected port
    baudrate = 9600  # Change this to your baudrate

    # Initialize serial connection
    ser = serial.Serial(port, baudrate)
    time.sleep(2)  # Wait for the serial connection to initialize

    for i, segment in enumerate(segment_vectors):
        for j, value in enumerate(segment):
            try:
                frame = prepare_frame(i, j, value, motor_speed)
                ser.write(frame)
                print(f"Sent frame for segment {i}, motor_id {j}, value {value}: {frame.hex().upper()}")
                time.sleep(0.001)
                # time.sleep(0.4)  # Delay between sending frames
            except ValueError as e:
                print(f"Error preparing frame for segment {i}, motor_id {j}, value {value}: {e}")

    # Close serial connection
    ser.close()

def send_calibration_frame(selected_port):
    try:
        # Serial port configuration
        port = selected_port.get()  # Get selected port
        baudrate = 9600  # Change this to your baudrate

        # Initialize serial connection
        ser = serial.Serial(port, baudrate)
        time.sleep(2)  # Wait for the serial connection to initialize

        # Prepare and send calibration frame
        calibration_frame = bytearray([0x55, 0xFF, 0xFF, 0x00, 0x00, 0xAA])  # Calibration frame data
        ser.write(calibration_frame)  # Send calibration frame
        print("Sent calibration frame:", calibration_frame.hex().upper())

        # Close serial connection
        ser.close()

    except Exception as e:
        messagebox.showerror("Błąd", "Wystąpił błąd podczas wysyłania ramki kalibracyjnej: {}".format(str(e)))

def create_segment_vector(dane, start_i, end_i, start_j, end_j, segment_name):
    segment = []
    for i in range(start_i, end_i):
        for j in range(start_j, end_j):
            segment.append(dane[i][j])
    return segment

def save_segment_vectors(segment_vectors, output_folder, filename):
    sciezka_pliku = output_folder + "/{}_32x16_segment_vectors.txt".format(filename)
    with open(sciezka_pliku, 'w') as plik:
        for segment_vector in segment_vectors:
            linia = ",".join(map(str, segment_vector))
            plik.write(linia + '\n')
    print("Segmenty zostały zapisane w pliku:", sciezka_pliku)

def save_frames(segment_vectors, motor_speed, output_folder, filename):
    sciezka_pliku = output_folder + "/{}_32x16_frames.bin".format(filename)
    with open(sciezka_pliku, 'wb') as plik:
        for i, segment in enumerate(segment_vectors):
            for j, value in enumerate(segment):
                frame = prepare_frame(i, j, value, motor_speed)
                plik.write(frame)
    print("Ramki zostały zapisane w pliku:", sciezka_pliku)

def select_input_files():
    input_paths = filedialog.askopenfilenames(title="Wybierz pliki wejściowe")
    for input_path in input_paths:
        listbox_input.insert(tk.END, input_path)

def select_output_folder():
    output_folder = filedialog.askdirectory(title="Wybierz folder wyjściowy")
    entry_output.delete(0, tk.END)
    entry_output.insert(0, output_folder)

# GUI setup
root = tk.Tk()
root.title("Konwersja obrazów")

label_input = tk.Label(root, text="Wybrane pliki wejściowe:")
label_input.grid(row=0, column=0, padx=5, pady=5, sticky="w")

listbox_input = tk.Listbox(root, width=50, height=10)
listbox_input.grid(row=0, column=1, padx=5, pady=5)

button_browse_input = tk.Button(root, text="Wybierz pliki", command=select_input_files)
button_browse_input.grid(row=0, column=2, padx=5, pady=5)

label_output = tk.Label(root, text="Folder wyjściowy:")
label_output.grid(row=1, column=0, padx=5, pady=5, sticky="w")

entry_output = tk.Entry(root, width=50)
entry_output.grid(row=1, column=1, padx=5, pady=5)

button_browse_output = tk.Button(root, text="Wybierz folder", command=select_output_folder)
button_browse_output.grid(row=1, column=2, padx=5, pady=5)

label_motor_speed_range = tk.Label(root, text="Prędkość silnika (od 0 do 255):")
label_motor_speed_range.grid(row=3, column=0, padx=5, pady=5, sticky="w")

motor_speed = tk.Entry(root, width=10)
motor_speed.grid(row=3, column=1, padx=5, pady=5)

label_port = tk.Label(root, text="Port COM:")
label_port.grid(row=4, column=0, padx=5, pady=5, sticky="w")

ports = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8"]  # Modify this list with available COM ports
selected_port = tk.StringVar(root)
selected_port.set(ports[0])  # Set default selected port

port_dropdown = tk.OptionMenu(root, selected_port, *ports)
port_dropdown.grid(row=4, column=1, padx=5, pady=5)

button_convert = tk.Button(root, text="Konwertuj", command=lambda: resize_and_convert_to_gray(listbox_input.get(0, tk.END), entry_output.get(), motor_speed, selected_port))
button_convert.grid(row=5, column=1, pady=10)

# Dodaj przycisk kalibracji
button_calibration = tk.Button(root, text="Kalibracja", command=lambda: send_calibration_frame(selected_port))
button_calibration.grid(row=6, column=1, pady=10)

button_exit = tk.Button(root, text="Wyjdź", command=root.destroy)
button_exit.grid(row=7, column=1, pady=10)

root.mainloop()
