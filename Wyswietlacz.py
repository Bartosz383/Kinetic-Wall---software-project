import tkinter as tk
import math
from tkinter import filedialog, simpledialog
from PIL import ImageColor
import random
# import test
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

        self.set_all_segments_to_zero()

        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=0, column=1, rowspan=5, padx=5)

        self.create_button(buttons_frame, "Rysuj", self.open_drawing_app)
        self.create_button(buttons_frame, "Ustaw wszystko na 0", self.set_all_segments_to_zero)
        self.create_button(buttons_frame, "Ustaw wszystko na 1", self.set_all_segments_to_one)
        self.create_button(buttons_frame, "Losowy wzór", self.create_pattern)
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

        self.show_display(self.hex_size)

    def create_button(self, frame, text, command):
        button = tk.Button(frame, text=text, command=command)
        button.pack(side="top")

    # def show_display(self):
    #     # Usunięcie istniejących prostokątów na canvasie
    #     self.canvas.delete("all")
    #
    #     # Wyświetlenie aktualnego stanu segmentów za pomocą wypełnionych prostokątów
    #     for i in range(16):
    #         for j in range(32):
    #             x1, y1 = j * 25, i * 25  # Zmienione rozmiary kafelków
    #             x2, y2 = x1 + 25, y1 + 25
    #
    #             color = "black" if self.segments[i][j] == 1 else "white"
    #
    #             self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    # def show_display(self, hex_size):
    #     # Usunięcie istniejących sześciokątów na canvasie
    #     self.canvas.delete("all")
    #
    #     # Wyświetlenie aktualnego stanu segmentów za pomocą wypełnionych sześciokątów
    #     for i in range(16):
    #         for j in range(32):
    #             x = j * 3 / 2 * self.hex_size
    #             y = i * math.sqrt(3) * self.hex_size
    #
    #             # Obrót co drugiego rzędu
    #             if j % 2 == 1:
    #                 y += math.sqrt(3) / 2 * self.hex_size
    #
    #             # Współrzędne wierzchołków sześciokąta
    #             hexagon_coords = [
    #                 x, y,
    #                 x + self.hex_size, y,
    #                 x + 3 / 2 * self.hex_size, y + math.sqrt(3) / 2 * self.hex_size,
    #                 x + self.hex_size, y + math.sqrt(3) * self.hex_size,
    #                 x, y + math.sqrt(3) * self.hex_size,
    #                 x - 1 / 2 * self.hex_size, y + math.sqrt(3) / 2 * self.hex_size
    #             ]
    #
    #             # Obliczenie poziomu szarości
    #             gray_level = self.segments[i][j]  # Przyjmuję, że self.segments zawiera wartości od 0 do 1
    #
    #             # Przekształcenie poziomu szarości na wartość RGB
    #             color = ImageColor.getrgb(
    #                 f'rgb({int(255 * gray_level)}, {int(255 * gray_level)}, {int(255 * gray_level)})')
    #
    #             # Narysowanie sześciokąta z odpowiednim wypełnieniem
    #             self.canvas.create_polygon(hexagon_coords, outline='black', fill=color)

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

    # def show_display(self, hex_size):
    #     # Usunięcie istniejących sześciokątów na canvasie
    #     self.canvas.delete("all")
    #
    #     # Wyświetlenie aktualnego stanu segmentów za pomocą wypełnionych sześciokątów
    #     for i in range(16):
    #         for j in range(32):
    #             x = j * 3 / 2 * self.hex_size
    #             y = i * math.sqrt(3) * self.hex_size
    #
    #             # Obrót co drugiego rzędu
    #             if j % 2 == 1:
    #                 y += math.sqrt(3) / 2 * self.hex_size
    #
    #             # Współrzędne wierzchołków sześciokąta
    #             hexagon_coords = [
    #                 x, y,
    #                 x + self.hex_size, y,
    #                 x + 3 / 2 * self.hex_size, y + math.sqrt(3) / 2 * self.hex_size,
    #                 x + self.hex_size, y + math.sqrt(3) * self.hex_size,
    #                 x, y + math.sqrt(3) * self.hex_size,
    #                 x - 1 / 2 * self.hex_size, y + math.sqrt(3) / 2 * self.hex_size
    #             ]
    #
    #             # Kolor wypełnienia
    #             color = "black" if self.segments[i][j] == 1 else "white"
    #
    #             # Narysowanie sześciokąta z odpowiednim wypełnieniem
    #             self.canvas.create_polygon(hexagon_coords, outline='black', fill=color)

    def create_pattern(self):
        # Tworzenie losowego wzoru z wartościami od 0 do 255
        pattern = [[random.randint(0, 255) for _ in range(32)] for _ in range(16)]

        self.segments = pattern
        self.show_display(self.hex_size)

    def set_all_segments_to_zero(self):
        # Ustawienie wszystkich segmentów na 0
        self.segments = [[0 for _ in range(32)] for _ in range(16)]
        self.show_display(self.hex_size)

    def set_all_segments_to_one(self):
        # Ustawienie wszystkich segmentów na 1
        self.segments = [[1 for _ in range(32)] for _ in range(16)]
        self.show_display(self.hex_size)

    def set_segments_to_pattern(self):
        # Ustawienie segmentów według określonego wzoru (np. jakieś konkretne wartości)
        # Poniżej znajduje się przykładowy wzór - można dostosować go do własnych potrzeb
        pattern = [
            [(i % 256) for i in range(32)] for _ in range(16)
        ]
        print(pattern)
        self.segments = pattern
        self.show_display(self.hex_size)

    def animate_wave(self, col=31):
        if col >= 0:
            self.set_all_segments_to_zero()

            for i in range(16):
                self.segments[i][col] = 1

            self.show_display()
            self.after(100, self.animate_wave, col - 1)
        else:
            self.set_all_segments_to_zero()

    def animate_double_wave(self, col1=31, col2=20):
        if col1 >= 0 and col2 >= 0:
            self.set_all_segments_to_zero()

            for i in range(16):
                self.segments[i][col1] = 1
                self.segments[i][col2] = 1

            self.show_display()
            self.after(100, self.animate_double_wave, col1 - 1, max(col2 - 1, 0))
        else:
            self.set_all_segments_to_zero()

    def Freelab_text(self):
        pattern = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
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
                pattern[int(transformed_y + i)][int(transformed_x + j)] = 1

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
