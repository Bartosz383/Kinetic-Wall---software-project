import tkinter as tk
from tkinter import filedialog, simpledialog

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing App")
        self.hex_size = 15  # rozmiar pół sześciokąta
        self.canvas_width = 32 * 3/2 * self.hex_size
        self.canvas_height = 16 * 3**0.5 * self.hex_size
        self.segments = [[0 for _ in range(32)] for _ in range(16)]  # inicjalizacja planszy segmentów
        self.drawings_library = []  # lista przechowująca rysunki

        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.canvas.bind("<B1-Motion>", self.draw_hex)  # rysowanie przy przeciśnięciu lewego przycisku myszy

        # self.save_button = tk.Button(self.master, text="Save Image", command=self.save_image)
        # self.save_button.grid(row=1, column=0)

        self.add_to_library_button = tk.Button(self.master, text="Dodaj do biblioteki", command=self.add_to_library)
        self.add_to_library_button.grid(row=1, column=1)

        self.display_library_button = tk.Button(self.master, text="Wyświetl bibliotekę", command=self.display_library)
        self.display_library_button.grid(row=1, column=2)

        self.clear_button = tk.Button(self.master, text="Wyczyść wszystko", command=self.clear_canvas)
        self.clear_button.grid(row=1, column=3)

        self.close_button = tk.Button(self.master, text="Zamknij", command=self.close_window)
        self.close_button.grid(row=1, column=4)

        self.draw_mode = True  # Początkowo tryb rysowania

        self.draw_mode_button = tk.Button(self.master, text="Switch to Erase Mode", command=self.toggle_draw_mode)
        self.draw_mode_button.grid(row=2, column=3)

    def toggle_draw_mode(self):
        self.draw_mode = not self.draw_mode
        if self.draw_mode:
            self.draw_mode_button.config(text="Switch to Erase Mode")
            self.canvas.bind("<B1-Motion>", self.draw_hex)
        else:
            self.draw_mode_button.config(text="Switch to Draw Mode")
            self.canvas.bind("<B1-Motion>", self.erase_hex)

    def draw_hex(self, event):
        if not self.draw_mode:
            return
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

    def erase_hex(self, event):
        if self.draw_mode:
            return
        i = int(event.y / (self.hex_size * 3 / 2))
        j = int(event.x / (self.hex_size * 3 / 2))
        if 0 <= i < 16 and 0 <= j < 32:
            x = j * 3 / 2 * self.hex_size
            y = i * 3 ** 0.5 * self.hex_size
            if j % 2 == 1:
                y += 3 ** 0.5 / 2 * self.hex_size
            hexagon_coords = [
                x, y,
                x + self.hex_size, y,
                x + 3 / 2 * self.hex_size, y + 3 ** 0.5 / 2 * self.hex_size,
                x + self.hex_size, y + 3 ** 0.5 * self.hex_size,
                x, y + 3 ** 0.5 * self.hex_size,
                x - 1 / 2 * self.hex_size, y + 3 ** 0.5 / 2 * self.hex_size
            ]
            self.canvas.create_polygon(hexagon_coords, outline='white', fill="white")
            self.segments[i][j] = 0

    def save_image(self):
        # zapisanie obrazka
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            # implementacja zapisu obrazka do pliku
            print("Image saved as", filename)

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
                print("    self.show_display(self.hex_size)\n")
        else:
            print("Library is empty.")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.segments = [[0 for _ in range(32)] for _ in range(16)]

    def close_window(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
