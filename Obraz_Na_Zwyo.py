import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import serial
import time
import threading
from queue import Queue

class YourClassName:
    def __init__(self):
        self.segments = None
        self.hex_size = None

    def Module_binary(self, normalized_matrix):
        self.segments = self.generate_segment_vectors(normalized_matrix)

    def generate_segment_vectors(self, pattern):
        segment_vectors = []
        for i in range(4):
            for j in range(8):
                segment_name = f"segment_{i * 8 + j}"
                segment = self.create_segment_vector(pattern, i * 4, (i + 1) * 4, j * 4, (j + 1) * 4)
                segment = [round(value, 2) for value in segment]  # Ograniczenie do 2 miejsc po przecinku
                segment_vectors.append((segment_name, segment))
        return segment_vectors

    def create_segment_vector(self, pattern, start_i, end_i, start_j, end_j):
        segment = []
        for i in range(start_i, end_i):
            for j in range(start_j, end_j):
                segment.append(pattern[i][j])
        return segment

# Funkcja do aktualizacji obrazu z kamery
def update_camera():
    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            video_label.imgtk = img
            video_label.config(image=img)
            video_label.update()
        time.sleep(0.03)  # Opóźnienie 30 ms (około 33 klatki na sekundę)

# Funkcja do aktualizacji etykiety z segmentami
def update_label():
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (32, 16))
        normalized = resized / 255.0
        # s_binary = cv2.resize(normalized, (320, 160))
        your_object = YourClassName()
        your_object.Module_binary(normalized)

        # Aktualizacja etykiety z segmentami
        segments_text = ""
        if your_object.segments:
            for segment_name, segment in your_object.segments:
                segment_str = ", ".join(map(str, segment))
                segments_text += f"{segment_name}: {segment_str}\n"
                # Dodawanie danych do kolejki dla portu COM3
                com_queue.put(segment_str)

        segment_label.config(text=segments_text)
        segment_label.update()
        time.sleep(0.03)  # Opóźnienie 30 ms (około 33 klatki na sekundę)

# Funkcja do wysyłania danych do portu szeregowego COM3
def send_to_serial():
    while True:
        data = com_queue.get()
        with serial.Serial('COM3', 9600, timeout=1) as ser:
            ser.write(data.encode())
            time.sleep(0.1)  # Poczekaj chwilę na wysłanie danych

# Funkcja do przygotowania ramki danych zaczynającej się od 0x55 i kończącej na 0xAA
def prepare_frame(bit2, bit3, bit4, bit5):
    checksum = calculate_xor_checksum(bit2, bit3, bit4, bit5)
    frame = bytearray([
        0x55,  # Start
        bit2,  # segment address
        bit3,  # motor address
        bit4,  # requested motor angle
        bit5,  # motor speed
        checksum,  # XOR checksum
        0xAA  # Stop
    ])
    return frame

# Funkcja do obliczania XOR checksum
def calculate_xor_checksum(bit2, bit3, bit4, bit5):
    return bit2 ^ bit3 ^ bit4 ^ bit5

# Rejestruj obraz z kamery i wyświetlaj go na żywo
cap = cv2.VideoCapture(0)

# Utwórz okno Tkinter
root = tk.Tk()
root.title("Segment Vector Display")

# Utwórz etykietę do wyświetlania segmentów
segment_label = tk.Label(root, text="", font=("Helvetica", 12), padx=10, pady=10)
segment_label.pack()

# Utwórz osobne okno dla obrazu z kamery
video_window = tk.Toplevel(root)
video_window.title("Camera Feed")
video_label = tk.Label(video_window)
video_label.pack()

# Utwórz kolejkę dla portu COM3
com_queue = Queue()

# Rozpocznij aktualizację obrazu z kamery w osobnym wątku
camera_thread = threading.Thread(target=update_camera)
camera_thread.daemon = True
camera_thread.start()

# Rozpocznij aktualizację etykiety z segmentami w osobnym wątku
label_thread = threading.Thread(target=update_label)
label_thread.daemon = True
label_thread.start()

# Rozpocznij wątek do wysyłania danych do portu COM3
serial_thread = threading.Thread(target=send_to_serial)
serial_thread.daemon = True
serial_thread.start()

# Pętla główna Tkintera
root.mainloop()

# Zatrzymaj odczyt z kamery
cap.release()
cv2.destroyAllWindows()

