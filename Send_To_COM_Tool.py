import tkinter as tk
from tkinter import filedialog, messagebox
import serial
import time


def select_files():
    global selected_files
    selected_files = filedialog.askopenfilenames(initialdir="/", title="Wybierz pliki")
    if selected_files:
        update_file_list_label()


def send_files():
    if not selected_files:
        messagebox.showinfo("Informacja", "Nie wybrano żadnych plików do wysłania.")
        return

    try:
        selected_port = port_entry.get()

        # Otwórz port szeregowy
        with serial.Serial(selected_port, baudrate=9600, timeout=1) as port:
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

        messagebox.showinfo("Sukces", "Pliki zostały wysłane pomyślnie przez port szeregowy.")

    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas wysyłania plików: {e}")


def update_file_list_label():
    if selected_files:
        file_list_label.config(text=f"Wybrane pliki: {', '.join(selected_files)}")
    else:
        file_list_label.config(text="Brak wybranych plików.")


# Główne okno GUI
root = tk.Tk()
root.title("Wysyłanie plików przez port szeregowy")

# Etykieta i przycisk do wyboru plików
select_files_button = tk.Button(root, text="Wybierz pliki", command=select_files)
select_files_button.grid(row=0, column=0, padx=5, pady=5)
file_list_label = tk.Label(root, text="Brak wybranych plików.")
file_list_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Etykieta i pole wyboru portu szeregowego
port_label = tk.Label(root, text="Wybierz port szeregowy:")
port_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
port_entry = tk.StringVar(root)
port_dropdown = tk.OptionMenu(root, port_entry, *["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8"])
port_dropdown.grid(row=2, column=1, padx=5, pady=5)

# Przycisk do wysyłania plików
send_files_button = tk.Button(root, text="Wyślij pliki", command=send_files)
send_files_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
