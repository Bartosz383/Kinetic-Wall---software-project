# # pattern = [
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #         ]
# #
# # def zmien_pole(tablica, wiersz, kolumna, nowa_wartosc):
# #     tablica[wiersz][kolumna] = nowa_wartosc
# #
# # def zmien_modul(n, k):
# #     for i in range(4):
# #         for j in range(4):
# #             zmien_pole(pattern, i + n, j + k, 42)
# #
# # # Wyświetlenie tablicy po zmianie
# # for row in pattern:
# #     print(row)
# #
# #
# #
# import tkinter as tk
# import math
# import random
#
# class TwoDimensionalArrayApp(tk.Tk):
#     def __init__(self):
#         super().__init__()
#
#         # Inicjalizacja zmiennych do przechowywania stanu segmentów
#         self.segments = [[random.randint(1, 9) for _ in range(32)] for _ in range(16)]
#
#         # Utworzenie canvas do rysowania segmentów
#         self.canvas = tk.Canvas(self, width=800, height=400)  # Zmieniony rozmiar canvasa
#         self.canvas.grid(row=0, column=0, rowspan=5)
#
#         # Inicjalizacja sześciokątnych obszarów (segmentów) na canvasie
#         self.hex_size = 20  # Rozmiar sześciokąta
#         self.draw_hexagons()
#
#     def draw_hexagons(self):
#         for row in range(len(self.segments)):
#             for col in range(len(self.segments[0])):
#                 x = col * 3/2 * self.hex_size
#                 y = row * math.sqrt(3) * self.hex_size
#
#                 # Obrót co drugiego rzędu
#                 if col % 2 == 1:
#                     y += math.sqrt(3) / 2 * self.hex_size
#
#                 # Współrzędne wierzchołków sześciokąta
#                 hexagon_coords = [
#                     x, y,
#                     x + self.hex_size, y,
#                     x + 3/2 * self.hex_size, y + math.sqrt(3) / 2 * self.hex_size,
#                     x + self.hex_size, y + math.sqrt(3) * self.hex_size,
#                     x, y + math.sqrt(3) * self.hex_size,
#                     x - 1/2 * self.hex_size, y + math.sqrt(3) / 2 * self.hex_size
#                 ]
#
#                 # Numer do wypełnienia w sześciokącie
#                 number = self.segments[row][col]
#
#                 # Narysowanie sześciokąta z wypełnieniem liczbą
#                 self.canvas.create_polygon(hexagon_coords, outline='black', fill='lightblue')
#                 self.canvas.create_text(x + self.hex_size, y + math.sqrt(3) / 2 * self.hex_size,
#                                         text=str(number), fill='black')
#
# if __name__ == "__main__":
#     app = TwoDimensionalArrayApp()
#     app.mainloop()

