import tkinter as tk
from tkinter import filedialog, messagebox
import serial
import time


def send_files():
    selected_files = filedialog.askopenfilenames(initialdir="/", title="Wybierz pliki")
    selected_port = port_entry.get()

    try:
        # Otwórz port szeregowy
        port = serial.Serial(selected_port, baudrate=9600, timeout=1)

        # Poczekaj 0,5 s przed rozpoczęciem przesyłania
        time.sleep(0.5)

        for selected_file in selected_files:
            # Otwórz wybrany plik i odczytaj jego zawartość jako binarną
            with open(selected_file, 'rb') as file:
                file_content = file.read()

            # Przesyłaj dane partiami po 14 znaków z przerwami 0,4 s
            chunk_size = 14
            for i in range(0, len(file_content), chunk_size):
                chunk = file_content[i:i + chunk_size]
                port.write(chunk)
                time.sleep(0.4)

        # Zamknij port szeregowy
        port.close()

        messagebox.showinfo("Sukces", "Pliki zostały wysłane pomyślnie przez port szeregowy.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas wysyłania plików: {e}")


root = tk.Tk()
root.title("Wysyłanie plików przez port szeregowy")

# Pole wyboru plików
file_label = tk.Label(root, text="Wybierz pliki do wysłania (po wybraniu zostaną natychmiast przesłane):")
file_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
browse_button = tk.Button(root, text="Przeglądaj", command=send_files)
browse_button.grid(row=0, column=1, padx=5, pady=5)

# Pole wyboru portu szeregowego
port_label = tk.Label(root, text="Wybierz port szeregowy:")
port_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
port_entry = tk.StringVar(root)
port_dropdown = tk.OptionMenu(root, port_entry, *["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8"])
port_dropdown.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()
