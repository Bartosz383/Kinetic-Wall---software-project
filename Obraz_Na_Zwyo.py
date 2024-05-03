import cv2
import numpy as np
import serial
import threading
import time
import tkinter as tk
from PIL import Image, ImageTk

# Ustawienia kamerki
CAMERA_INDEX = 0  # Indeks kamery, domyślnie 0 (pierwsza dostępna kamera)

# Ustawienia przesyłania przez port szeregowy
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

# Ustawienia obrazu
TARGET_WIDTH = 32
TARGET_HEIGHT = 16

# Klasa obsługująca główne okno aplikacji
class Application:
    def __init__(self, window, video_source=0):
        self.window = window
        self.window.title("Camera Viewer")

        # Utwórz obiekt kamery
        self.vid = Camera(video_source)

        # Utwórz etykietę do wyświetlania obrazu
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Przycisk rozpoczęcia transmisji
        self.start_btn = tk.Button(window, text="Start Transmission", width=20, command=self.start_transmission)
        self.start_btn.pack(anchor=tk.CENTER, expand=True)

        # Przycisk zakończenia transmisji
        self.stop_btn = tk.Button(window, text="Stop Transmission", width=20, command=self.stop_transmission, state=tk.DISABLED)
        self.stop_btn.pack(anchor=tk.CENTER, expand=True)

        # Przycisk zakończenia programu
        self.quit_button = tk.Button(window, text="Quit", width=20, command=self.quit)
        self.quit_button.pack(anchor=tk.CENTER, expand=True)

        # Pole do wprowadzania prędkości silnika
        self.motor_speed_label = tk.Label(window, text="Motor Speed: (by zmienić należy zatrzymać transmisje)")
        self.motor_speed_label.pack(anchor=tk.CENTER, expand=True)
        self.motor_speed_entry = tk.Entry(window)
        self.motor_speed_entry.pack(anchor=tk.CENTER, expand=True)

        # Ustaw domyślną wartość prędkości silnika
        self.motor_speed_entry.insert(0, "100")

        self.streaming = False
        self.thread = None

        self.update()

        # Obsługa zdarzenia zamknięcia okna
        self.window.protocol("WM_DELETE_WINDOW", self.quit)

    def start_transmission(self):
        if not self.streaming:
            # Pobierz wartość prędkości silnika z pola wprowadzania
            motor_speed = int(self.motor_speed_entry.get())

            self.streaming = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.thread = threading.Thread(target=self.transmit, args=(motor_speed,))
            self.thread.start()

    def stop_transmission(self):
        if self.streaming:
            self.streaming = False
            self.stop_btn.config(state=tk.DISABLED)
            self.start_btn.config(state=tk.NORMAL)

    def quit(self):
        if self.streaming:
            self.streaming = False
            self.thread.join()  # Zaczekaj, aż wątek transmisji zakończy działanie

        self.window.destroy()

    def update(self):
        # Pobierz klatkę z kamery
        ret, frame = self.vid.get_frame()

        if ret:
            # Konwertuj klatkę na obiekt ImageTk i wyświetl na Canvas
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)

    def transmit(self, motor_speed):
        try:
            # Otwórz połączenie szeregowe
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
            print("Serial port opened")

            while self.streaming:
                ret, frame = self.vid.get_frame()

                if ret:
                    # Konwertuj klatkę na monochromatyczną, przeskaluj i normalizuj
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    scaled_frame = cv2.resize(gray_frame, (TARGET_WIDTH, TARGET_HEIGHT))
                    normalized_frame = cv2.normalize(scaled_frame, None, 0, 255, cv2.NORM_MINMAX)

                    # Podziel obraz na segmenty i przekaż każdy segment do funkcji prepare_frame
                    for i in range(4):
                        for j in range(8):
                            segment = normalized_frame[i * 4:(i + 1) * 4, j * 4:(j + 1) * 4]
                            bit2 = i  # segment address
                            bit3 = j          # motor address (wartości od 0 do 15, iterowane w kółko)
                            bit4 = np.mean(segment)  # requested motor angle; value (segment)
                            bit5 = motor_speed        # motor speed

                            # Przygotuj ramkę danych
                            frame_data = prepare_frame(bit2, bit3, int(bit4), bit5)

                            # Prześlij ramkę danych przez port szeregowy
                            ser.write(frame_data)

                time.sleep(0.1)

        except serial.SerialException as e:
            print("Error opening serial port:", e)

        finally:
            if ser.is_open:
                ser.close()
                print("Serial port closed")

# Funkcja tworząca ramkę danych
def prepare_frame(segment_address, motor_address, requested_motor_angle, motor_speed):
    # Oblicz XOR checksum
    checksum = calculate_xor_checksum(segment_address, motor_address, requested_motor_angle, motor_speed)

    # Utwórz ramkę danych
    frame = bytearray([
        0x55,                    # Start
        segment_address,         # Adres segmentu
        motor_address,           # Adres silnika (wartości od 0 do 15, iterowane w kółko)
        requested_motor_angle,  # Wartość żądanego kąta silnika (segmentu)
        motor_speed,             # Prędkość silnika
        checksum,                # XOR checksum
        0xAA                     # Stop
    ])

    return frame

# Funkcja obliczająca XOR checksum
def calculate_xor_checksum(*bits):
    # Oblicz XOR checksum dla podanych bitów
    checksum = 0
    for bit in bits:
        checksum ^= bit
    return checksum

# Klasa obsługująca kamerę
class Camera:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open camera")

        # Ustaw rozmiar obrazu
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None
        else:
            return None, None

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Uruchom aplikację
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root, video_source=CAMERA_INDEX)
    root.mainloop()
