import tkinter as tk
from tkinter import filedialog, messagebox
import serial
import time


class FileSenderApp:
    def __init__(self):
        self.selected_files = []
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Wysyłanie plików przez port szeregowy")

        self.select_files_button = tk.Button(self.root, text="Wybierz pliki", command=self.select_files)
        self.select_files_button.grid(row=0, column=0, padx=5, pady=5)
        self.file_list_label = tk.Label(self.root, text="Brak wybranych plików.")
        self.file_list_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.port_label = tk.Label(self.root, text="Wybierz port szeregowy:")
        self.port_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.port_entry = tk.StringVar(self.root)
        self.port_dropdown = tk.OptionMenu(self.root, self.port_entry, *["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8"])
        self.port_dropdown.grid(row=2, column=1, padx=5, pady=5)

        self.send_files_button = tk.Button(self.root, text="Wyślij pliki", command=self.send_files)
        self.send_files_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def select_files(self):
        self.selected_files = filedialog.askopenfilenames(initialdir="/", title="Wybierz pliki")
        if self.selected_files:
            self.update_file_list_label()

    def send_files(self):
        if not self.selected_files:
            messagebox.showinfo("Informacja", "Nie wybrano żadnych plików do wysłania.")
            return

        try:
            selected_port = self.port_entry.get()

            # Otwórz port szeregowy
            with serial.Serial(selected_port, baudrate=9600, timeout=1) as port:
                # Poczekaj 0,5 s przed rozpoczęciem przesyłania
                time.sleep(0.5)

                for selected_file in self.selected_files:
                    # Otwórz wybrany plik i odczytaj jego zawartość jako binarną
                    with open(selected_file, 'rb') as file:
                        file_content = file.read()

                    # Przesyłaj dane partiami po 14 znaków z przerwami 0,4 s
                    chunk_size = 14
                    for i in range(0, len(file_content), chunk_size):
                        chunk = file_content[i:i + chunk_size]
                        port.write(chunk)
                        time.sleep(0.4)

            messagebox.showinfo("Sukces", "Pliki zostały wysłane pomyślnie przez port szeregowy.")

        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas wysyłania plików: {e}")

    def update_file_list_label(self):
        if self.selected_files:
            self.file_list_label.config(text=f"Wybrane pliki: {', '.join(self.selected_files)}")
        else:
            self.file_list_label.config(text="Brak wybranych plików.")


if __name__ == "__main__":
    app = FileSenderApp()
    app.root.mainloop()
