import tkinter as tk
import math
from tkinter import filedialog, simpledialog
import Uzytkownik
from PIL import ImageColor
import random
import serial
import time

class DisplayWindow(tk.Tk):
    def __init__(self, modul_name):
        super().__init__()

        self.title(modul_name)
        self.geometry("1000x450")  # Zmieniony rozmiar okna

        # Inicjalizacja zmiennych do przechowywania stanu segmentów
        # self.segments = [[0 for _ in range(32)] for _ in range(16)]

        # Utworzenie canvas do rysowania segmentów
        self.canvas = tk.Canvas(self, width=800, height=600)  # Zmieniony rozmiar canvasa
        self.canvas.grid(row=0, column=0, rowspan=5)

        self.hex_size = 15  # Rozmiar sześciokąta
        self.drawings_library = []  # lista przechowująca rysunki

        self.set_all_segments_to_white()

        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=0, column=1, rowspan=5, padx=5)

        # self.create_button(buttons_frame, "Wyślij ramki", self.send_frames)
        # stwórz przycisk, który wywołuje funkcje send frames
        # wszystkim funkcją odbierz send frames
        # stwórz funkcje send frames dla COM3 albo daj funkcje pozwalającą na wybór portu szeregowego
        self.create_button(buttons_frame, "Rysuj", self.open_drawing_app)
        self.create_button(buttons_frame, "Ustaw wszystko na 0", self.set_all_segments_to_white)
        self.create_button(buttons_frame, "Ustaw wszystko na 1", self.set_all_segments_to_black)
        self.create_button(buttons_frame, "Losowy wzór", self.create_random_pattern)
        self.create_button(buttons_frame, "Ustaw według wzoru", self.set_segments_to_pattern)
        # self.create_button(buttons_frame, "Animuj falę", self.animate_wave)
        # self.create_button(buttons_frame, "Animuj podwójną falę", self.animate_double_wave)
        self.create_button(buttons_frame, "Wyświetl napis Freelab", self.Freelab_text)
        self.create_button(buttons_frame, "Przesun w dół", self.shift_down)
        self.create_button(buttons_frame, "Przesun w górę", self.shift_up)
        self.create_button(buttons_frame, "Przesun w lewo", self.shift_left)
        self.create_button(buttons_frame, "Przesun w prawo", self.shift_right)
        self.create_button(buttons_frame, "Animuj", self.animate)
        self.create_button(buttons_frame, "Animuj kilka razy", self.animate_loop)

        # self.create_button(buttons_frame, "Zmien modul", self.zmien_modul)

        # self.show_display(self.hex_size, self.send_frames)


    def create_button(self, frame, text, command):
        button = tk.Button(frame, text=text, command=command)
        button.pack(side="top")

    def show_display(self, hex_size):
        # Usunięcie istniejących sześciokątów na canvasie
        self.canvas.delete("all")

        # Wyświetlenie aktualnego stanu segmentów za pomocą wypełnionych sześciokątów
        for i in range(16):
            for j in range(32):
                x = j * 3 / 2 * self.hex_size
                y = i * math.sqrt(3) * self.hex_size

                # Obrót co drugiego rzędu
                if j % 2 == 1:
                    y += math.sqrt(3) / 2 * self.hex_size

                # Współrzędne wierzchołków sześciokąta
                hexagon_coords = [
                    x, y,
                    x + self.hex_size, y,
                    x + 3 / 2 * self.hex_size, y + math.sqrt(3) / 2 * self.hex_size,
                    x + self.hex_size, y + math.sqrt(3) * self.hex_size,
                    x, y + math.sqrt(3) * self.hex_size,
                    x - 1 / 2 * self.hex_size, y + math.sqrt(3) / 2 * self.hex_size
                ]

                # Kolor wypełnienia
                grayscale_value = self.segments[i][j]  # Wartość segmentu z zakresu od 0 do 255
                grayscale_hex = "#{:02x}{:02x}{:02x}".format(255 - grayscale_value, 255 - grayscale_value,
                                                             255 - grayscale_value)  # Odwrotność wartości
                color = grayscale_hex  # Ustawienie koloru wypełnienia na wartość odpowiadającą odwrotności wartości segmentu

                # Narysowanie sześciokąta z odpowiednim wypełnieniem
                self.canvas.create_polygon(hexagon_coords, outline='black', fill=color)

                # Pobranie wektorów segmentów i ich wypisanie
                segment_vectors = self.get_segment_vectors()
                for vector in segment_vectors:
                    print(vector)
                    pass
                # send_frames(segment_vectors, 100,"COM3")

    def get_segment_vectors(self):
        # Zwraca wektory segmentów z tablicy segments
        segment_vectors = [
            self.create_segment_vector(self.segments, i * 4, (i + 1) * 4, j * 4, (j + 1) * 4,
                                       f"segment_{i * 8 + j}")
            for i in range(4)
            for j in range(8)
        ]
        return segment_vectors

    def create_segment_vector(self, dane, start_i, end_i, start_j, end_j, segment_name):
        segment = []
        for i in range(start_i, end_i):
            for j in range(start_j, end_j):
                segment.append(dane[i][j])
        return segment

    def calculate_xor_checksum(self, bit2, bit3, bit4, bit5):
        print(bit2 ^ bit3 ^ bit4 ^ bit5)
        return bit2 ^ bit3 ^ bit4 ^ bit5

    def prepare_frame(self, bit2, bit3, bit4, bit5):
        checksum = self.calculate_xor_checksum(bit2, bit3, bit4, bit5)
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

    def send_frames(self, segment_vectors, motor_speed, selected_port):
        # Serial port configuration
        port = selected_port  # Change this to the selected port
        baudrate = 9600  # Change this to your baudrate

        try:
            # Initialize serial connection
            ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Wait for the serial connection to initialize

            for i, segment in enumerate(segment_vectors):
                for j, value in enumerate(segment):
                    try:
                        frame = self.prepare_frame(i, j, value, motor_speed)
                        ser.write(frame)
                        print(f"Sent frame for segment {i}, motor_id {j}, value {value}: {frame.hex().upper()}")
                        time.sleep(0.01)  # Delay between sending frames
                    except ValueError as e:
                        print(f"Error preparing frame for segment {i}, motor_id {j}, value {value}: {e}")

            # Close serial connection
            ser.close()
        except serial.SerialException as e:
            print(f"Could not open serial port {port}: {e}")

    def create_random_pattern(self):
        # Tworzenie losowego wzoru z wartościami od 0 do 255
        pattern = [[random.randint(0, 255) for _ in range(32)] for _ in range(16)]

        self.segments = pattern
        self.show_display(self.hex_size)


    def set_all_segments_to_white(self):
        # Ustawienie wszystkich segmentów na 0
        self.segments = [[0 for _ in range(32)] for _ in range(16)]
        self.show_display(self.hex_size)

    def set_all_segments_to_black(self):
        # Ustawienie wszystkich segmentów na 1
        self.segments = [[255 for _ in range(32)] for _ in range(16)]
        self.show_display(self.hex_size)

    def set_segments_to_pattern(self):
        pattern = [
            [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248],
            [45, 12, 182, 77, 99, 94, 135, 158, 223, 42, 162, 158, 67, 238, 32, 150, 143, 2, 149, 169, 150, 149, 59, 119, 77, 154, 144, 228, 71, 111, 236, 55],
            [50, 42, 9, 8, 211, 138, 84, 0, 29, 122, 43, 190, 242, 86, 151, 165, 116, 75, 34, 67, 236, 249, 69, 61, 169, 195, 239, 22, 217, 185, 226, 59],
            [50, 42, 9, 8, 211, 138, 84, 0, 29, 122, 43, 190, 242, 86, 151, 165, 116, 75, 34, 67, 236, 249, 69, 61, 169, 195, 239, 22, 217, 185, 226, 59],
            [50, 42, 9, 8, 211, 138, 84, 0, 29, 122, 43, 190, 242, 86, 151, 165, 116, 75, 34, 67, 236, 249, 69, 61, 169, 195, 239, 22, 217, 185, 226, 59],
            [50, 42, 9, 8, 211, 138, 84, 0, 29, 122, 43, 190, 242, 86, 151, 165, 116, 75, 34, 67, 236, 249, 69, 61, 169, 195, 239, 22, 217, 185, 226, 59],
            [50, 42, 9, 8, 211, 138, 84, 0, 29, 122, 43, 190, 242, 86, 151, 165, 116, 75, 34, 67, 236, 249, 69, 61, 169, 195, 239, 22, 217, 185, 226, 59],
            [92, 242, 8, 132, 173, 5, 244, 59, 41, 69, 154, 40, 50, 248, 176, 89, 73, 139, 180, 186, 157, 77, 22, 184, 58, 93, 20, 57, 21, 234, 166, 78],
            [43, 233, 33, 244, 242, 73, 60, 138, 67, 156, 225, 75, 231, 227, 136, 20, 71, 78, 239, 212, 217, 34, 132, 124, 200, 53, 210, 124, 223, 210, 179, 222],
            [231, 186, 173, 182, 98, 105, 3, 19, 244, 62, 153, 192, 141, 108, 79, 150, 25, 219, 233, 216, 143, 247, 198, 83, 95, 231, 113, 60, 196, 207, 43, 223],
            [126, 3, 40, 136, 117, 88, 39, 72, 106, 34, 159, 172, 11, 194, 98, 38, 252, 32, 122, 88, 18, 132, 157, 187, 120, 244, 215, 58, 117, 198, 188, 232],
            [ 179, 254, 97, 241, 118, 108, 212, 133, 240, 73, 125, 129, 211, 58, 201, 31, 35, 241, 101, 154, 93, 184, 188, 36, 96, 194, 49, 239, 37, 178, 94, 47],
            [41, 185, 61, 223, 151, 151, 3, 247, 165, 156, 24, 17, 120, 120, 10, 5, 117, 67, 11, 214, 123, 42, 250, 161, 83, 212, 9, 84, 191, 89, 239, 34],
            [45, 200, 36, 251, 142, 79, 237, 233, 54, 46, 77, 138, 59, 208, 247, 222, 105, 218, 24, 34, 226, 113, 178, 208, 107, 179, 129, 32, 169, 126, 20, 130],
            [192, 207, 164, 226, 68, 163, 234, 238, 63, 62, 190, 127, 22, 11, 60, 17, 172, 253, 184, 141, 20, 217, 116, 10, 191, 37, 17, 204, 170, 133, 209, 160],
            [108, 100, 137, 59, 4, 201, 71, 78, 107, 2, 117, 71, 26, 224, 10, 23, 45, 194, 70, 34, 187, 46, 176, 11, 44, 75, 73, 108, 62, 70, 253, 174]
        ]

        self.segments = pattern
        self.show_display(self.hex_size)

    def animate_wave(self, col=31):
        if col >= 0:
            self.set_all_segments_to_white()

            for i in range(16):
                self.segments[i][col] = 1

            self.show_display()
            self.after(100, self.animate_wave, col - 1)
        else:
            self.set_all_segments_to_white()

    def animate_double_wave(self, col1=31, col2=20):
        if col1 >= 0 and col2 >= 0:
            self.set_all_segments_to_white()

            for i in range(16):
                self.segments[i][col1] = 1
                self.segments[i][col2] = 1

            self.show_display()
            self.after(100, self.animate_double_wave, col1 - 1, max(col2 - 1, 0))
        else:
            self.set_all_segments_to_white()

    def Freelab_text(self):
        pattern = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 0, 0, 255, 255, 255, 0, 255, 255, 255, 255, 0, 0],
            [0, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 255, 255, 255, 0, 0],
            [0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0, 0,255, 0, 0],
            [0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 0, 0],
            [0, 255, 255, 255, 0, 255, 255, 255, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 0, 255, 0, 0, 255, 0, 0],
            [0, 255, 255, 255, 0, 255, 255, 255, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 255, 255, 255, 0, 0],
            [0, 255, 0, 0, 0, 255, 0, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 0],
            [0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 0],
            [0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0],
            [0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0],
            [0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0],
            [0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0, 255, 0, 0, 0, 255, 0],
            [0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 0],
            [0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 255, 255, 0, 255, 0, 255, 0, 255, 255, 255, 255, 255, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.segments = pattern
        self.show_display(self.hex_size)

    def Module_0_On(self):
        pattern = [
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.segments = pattern
        self.show_display(self.hex_size)

    # def binary_pattern(self):
    #     pattern = test.binary
    #
    #     self.segments = pattern
    #     self.show_display(self.hex_size)
    def shift_down(self, n=1):
        # Przesuwanie wierszy
        self.segments = self.segments[-n:] + self.segments[:-n]
        self.show_display(self.hex_size)

    def shift_up(self, n=1):
        # Przesuwanie wierszy
        self.segments = self.segments[n:] + self.segments[:n]
        self.show_display(self.hex_size)

    def shift_left(self, n=1):
        # Przesuwanie kolumn
        self.segments = [row[n:] + row[:n] for row in self.segments]
        self.show_display(self.hex_size)

    def shift_right(self, n=1):
        # Przesuwanie kolumn
        self.segments = [row[-n:] + row[:-n] for row in self.segments]
        self.show_display(self.hex_size)

    def animate(self, col=31):
        if col >= 0:
            self.shift_right(1)
            self.after(100, self.animate, col - 1)
        else:
            self.shift_right(0)

    def animate_loop(self, col=62):
        if col >= 0:
            self.shift_right(1)
            self.after(100, self.animate, col - 1)
            self.shift_right(1)
        else:
            self.shift_right(0)
    def zmien_modul(self, transformed_x, transformed_y):
        pattern_size = 4  # Wielkość obszaru wypełnionego jedynkami
        pattern = [[0] * 32 for _ in range(16)]

        # Ogranicz wartość x do przedziału 0-28
        x = max(0, min(transformed_x, 32))

        # Ogranicz wartość y do przedziału 0-12
        y = max(0, min(transformed_y, 16))

        for i in range(pattern_size):
            for j in range(pattern_size):
                pattern[int(transformed_y + i)][int(transformed_x + j)] = 255

        self.segments = pattern
        self.show_display(self.hex_size)

    def open_drawing_app(self):
        self.drawing_app_window = tk.Toplevel(self)
        self.drawing_app_window.title("Rysowanie")

        self.hex_size = 15  # Rozmiar sześciokąta
        hex_width = 3 / 2 * self.hex_size
        hex_height = math.sqrt(3) * self.hex_size

        self.canvas = tk.Canvas(self.drawing_app_window, width=32 * hex_width, height=16 * hex_height + 10)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        self.canvas.bind("<Button-1>", self.paint_hex)
        self.canvas.bind("<B1-Motion>", self.paint_hex)

        # Przycisk do przełączania między rysowaniem a mazaniem
        self.draw_mode = True  # Początkowy stan: rysowanie
        self.mode_button = tk.Button(self.drawing_app_window, text="Rysuj", command=self.toggle_mode)
        self.mode_button.pack()
        self.clear_button = tk.Button(self.drawing_app_window, text="Wyczyść tablicę", command=self.clear_canvas)
        self.clear_button.pack()
        self.add_to_library_button = tk.Button(self.drawing_app_window, text="Zapisz do pamięci programu", command=self.add_to_library)
        self.add_to_library_button.pack()

        self.show_display(self.hex_size)

    def toggle_mode(self):
        # Przełączanie między rysowaniem a mazaniem
        self.draw_mode = not self.draw_mode
        if self.draw_mode:
            self.mode_button.config(text="Rysuj")
        else:
            self.mode_button.config(text="Mazanie")

    def paint_hex(self, event):
        # Przetwarzanie współrzędnych kliknięcia na indeksy hexa
        hex_width = 3 / 2 * self.hex_size
        hex_height = math.sqrt(3) * self.hex_size
        col = int(event.x / hex_width)
        row = int(event.y / hex_height)
        if col % 2 == 1:
            row -= 1

        # Sprawdzenie czy współrzędne są w zakresie 16x32
        if 0 <= col < 32 and 0 <= row < 16:
            # Obliczanie współrzędnych sześciokąta
            x = col * hex_width
            y = row * (hex_height)
            if col % 2 == 1:
                y += hex_height / 2

            # Rysowanie lub mazanie sześciokąta, w zależności od aktualnego stanu
            if self.draw_mode:
                color = "black"
            else:
                color = self.canvas.cget('bg')
            hexagon_coords = [
                x, y,
                x + self.hex_size, y,
                x + hex_width, y + hex_height / 2,
                x + self.hex_size, y + hex_height,
                x, y + hex_height,
                x - hex_width / 2, y + hex_height / 2
            ]
            self.canvas.create_polygon(hexagon_coords, outline='black', fill=color)

    def clear_canvas(self):
        # Usunięcie wszystkich elementów związanych z sześciokątami z canvasa
        self.canvas.delete("all")
        self.show_display(self.hex_size)
    def add_to_library(self):
        # Dodanie obrazka do biblioteki
        name = simpledialog.askstring("Input", "Enter image name:")
        if name:
            self.drawings_library.append((name, self.segments.copy()))  # Zapisanie nazwy i kopii rysunku
            print("Image added to library with name:", name)

            # Zapisanie kodu funkcji do pliku "Uzytkownik.py"
            filename = "Uzytkownik.py"
            with open(filename, "a") as file:
                file.write(f"\ndef {name}(self):\n")
                file.write("    pattern = [\n")
                for row in self.segments:
                    file.write("        " + str(row) + ",\n")
                file.write("    ]\n\n")
                file.write("    self.segments = pattern\n")
                file.write("    self.show_display(self.hex_size)\n")
            print(f"Code appended to {filename}")

if __name__ == "__main__":
    display_window = DisplayWindow(modul_name="Wszystkie moduły")
    display_window.mainloop()

