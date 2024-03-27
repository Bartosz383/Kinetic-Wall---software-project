import tkinter as tk
from tkinter import filedialog, simpledialog

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing App")
        self.hex_size = 20  # rozmiar pół sześciokąta
        self.canvas_width = 32 * 3/2 * self.hex_size
        self.canvas_height = 16 * 3**0.5 * self.hex_size
        self.segments = [[0 for _ in range(32)] for _ in range(16)]  # inicjalizacja planszy segmentów
        self.drawings_library = []  # lista przechowująca rysunki

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.draw_hex)  # rysowanie przy przeciśnięciu lewego przycisku myszy

        self.save_button = tk.Button(self.master, text="Save Image", command=self.save_image)
        self.save_button.pack()

        self.add_to_library_button = tk.Button(self.master, text="Add to Library", command=self.add_to_library)
        self.add_to_library_button.pack()

        self.display_library_button = tk.Button(self.master, text="Display Library", command=self.display_library)
        self.display_library_button.pack()

    def draw_hex(self, event):
        # obliczenie indeksów segmentu na podstawie pozycji myszy
        i = int(event.y / (self.hex_size * 3/2))
        j = int(event.x / (self.hex_size * 3/2))

        # sprawdzenie czy współrzędne mieszczą się w obszarze 16x32
        if 0 <= i < 16 and 0 <= j < 32:
            # rysowanie pół sześciokąta w odpowiednim miejscu
            x = j * 3/2 * self.hex_size
            y = i * 3**0.5 * self.hex_size
            if j % 2 == 1:
                y += 3**0.5 / 2 * self.hex_size

            hexagon_coords = [
                x, y,
                x + self.hex_size, y,
                x + 3/2 * self.hex_size, y + 3**0.5 / 2 * self.hex_size,
                x + self.hex_size, y + 3**0.5 * self.hex_size,
                x, y + 3**0.5 * self.hex_size,
                x - 1/2 * self.hex_size, y + 3**0.5 / 2 * self.hex_size
            ]

            self.canvas.create_polygon(hexagon_coords, outline='black', fill="black")

            # aktualizacja stanu segmentu
            self.segments[i][j] = 1

    def save_image(self):
        # zapisanie obrazka
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            # implementacja zapisu obrazka do pliku
            print("Image saved as", filename)

    def add_to_library(self):
        # dodanie obrazka do biblioteki
        name = simpledialog.askstring("Input", "Enter image name:")
        if name:
            self.drawings_library.append((name, self.segments.copy()))  # zapisanie nazwy i kopii rysunku
            print("Image added to library with name:", name)

    def display_library(self):
        # wyświetlenie biblioteki
        if self.drawings_library:
            print("Drawings in library:")
            for name, drawing in self.drawings_library:
                print("def ", name, "(self):")
                print("    pattern = [")
                for row in drawing:
                    print("        " + str(row) + ",")
                print("    ]")
                print("    self.segments = pattern")
                print("    self.show_display(self.hex_size)")
        else:
            print("Library is empty.")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
