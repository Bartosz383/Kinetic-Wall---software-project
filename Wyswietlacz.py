import tkinter as tk

class DisplayWindow(tk.Tk):
    def __init__(self, modul_name):
        super().__init__()

        self.title(modul_name)
        self.geometry("550x400")

        # Inicjalizacja zmiennych do przechowywania stanu segmentów
        self.segments = [[0 for _ in range(4)] for _ in range(4)]

        # Utworzenie canvas do rysowania segmentów
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.grid(row=0, column=0, rowspan=5)

        # Przyciski do ustawienia wszystkich segmentów na 0, 1 oraz według wzoru
        zero_button = tk.Button(self, text="Ustaw wszystko na 0", command=self.set_all_segments_to_zero)
        zero_button.grid(row=0, column=1, columnspan=2)

        one_button = tk.Button(self, text="Ustaw wszystko na 1", command=self.set_all_segments_to_one)
        one_button.grid(row=1, column=1, columnspan=2)

        pattern_button = tk.Button(self, text="Ustaw według wzoru", command=self.set_segments_to_pattern)
        pattern_button.grid(row=2, column=1, columnspan=2)

        pattern0_button = tk.Button(self, text="Ustaw według wzoru", command=self.set_pattern_0)
        pattern0_button.grid(row=3, column=1, columnspan=2)

        # Wywołanie funkcji, aby zainicjować widok
        self.show_display()

    def show_display(self):
        # Usunięcie istniejących prostokątów na canvasie
        self.canvas.delete("all")

        # Wyświetlenie aktualnego stanu segmentów za pomocą wypełnionych prostokątów
        for i in range(4):
            for j in range(4):
                x1, y1 = j * 100, i * 100
                x2, y2 = x1 + 100, y1 + 100

                color = "black" if self.segments[i][j] == 1 else "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def set_all_segments_to_zero(self):
        # Ustawienie wszystkich segmentów na 0
        self.segments = [[0 for _ in range(4)] for _ in range(4)]
        self.show_display()

    def set_all_segments_to_one(self):
        # Ustawienie wszystkich segmentów na 1
        self.segments = [[1 for _ in range(4)] for _ in range(4)]
        self.show_display()

    def set_segments_to_pattern(self):
        # Ustawienie segmentów według określonego wzoru (np. jakieś konkretne wartości)
        # Poniżej znajduje się przykładowy wzór - można dostosować go do własnych potrzeb
        pattern = [
            [1, 0, 0, 1],
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [0, 1, 1, 0]
        ]

        self.segments = pattern
        self.show_display()

    def set_pattern_0(self):
        # Ustawienie segmentów według określonego wzoru (np. jakieś konkretne wartości)
        # Poniżej znajduje się przykładowy wzór - można dostosować go do własnych potrzeb
        pattern = [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0]
        ]

        self.segments = pattern
        self.show_display()

if __name__ == "__main__":
    display_window = DisplayWindow(modul_name="Modul 1")
    display_window.mainloop()
