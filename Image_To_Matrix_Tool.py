# import cv2
# import tkinter as tk
# from tkinter import filedialog
#
#
# def resize_and_convert_to_gray(input_paths, output_folder):
#     for input_path in input_paths:
#         # Wczytanie obrazu
#         original_image = cv2.imread(input_path)
#
#         # Zmiana rozmiaru na 32x16
#         resized_image_32x16 = cv2.resize(original_image, (32, 16))
#
#         # Zmiana rozmiaru na 320x160
#         resized_image_320x160 = cv2.resize(original_image, (320, 160))
#
#         # Konwersja obrazów na skalę szarości
#         gray_image_32x16 = cv2.cvtColor(resized_image_32x16, cv2.COLOR_BGR2GRAY)
#         gray_image_320x160 = cv2.cvtColor(resized_image_320x160, cv2.COLOR_BGR2GRAY)
#
#         # Pobranie nazwy pliku bez ścieżki
#         filename = input_path.split("/")[-1]
#
#         # Zapis obrazów do plików
#         cv2.imwrite(output_folder + "/{}_32x16.jpg".format(filename), gray_image_32x16)
#         cv2.imwrite(output_folder + "/{}_320x160.jpg".format(filename), gray_image_320x160)
#     print("Konwersja zakończona pomyślnie.")
#
#
#
# def select_input_files():
#     input_paths = filedialog.askopenfilenames(title="Wybierz pliki wejściowe")
#     for input_path in input_paths:
#         listbox_input.insert(tk.END, input_path)
#
#
# def select_output_folder():
#     output_folder = filedialog.askdirectory(title="Wybierz folder wyjściowy")
#     entry_output.delete(0, tk.END)
#     entry_output.insert(0, output_folder)
#
#
# # Tworzenie głównego okna Tkinter
# root = tk.Tk()
# root.title("Konwersja obrazów")
#
# # Etykiety i pola do wprowadzania ścieżek
# label_input = tk.Label(root, text="Wybrane pliki wejściowe:")
# label_input.grid(row=0, column=0, padx=5, pady=5, sticky="w")
#
# listbox_input = tk.Listbox(root, width=50, height=10)
# listbox_input.grid(row=0, column=1, padx=5, pady=5)
#
# button_browse_input = tk.Button(root, text="Wybierz pliki", command=select_input_files)
# button_browse_input.grid(row=0, column=2, padx=5, pady=5)
#
# label_output = tk.Label(root, text="Folder wyjściowy:")
# label_output.grid(row=1, column=0, padx=5, pady=5, sticky="w")
#
# entry_output = tk.Entry(root, width=50)
# entry_output.grid(row=1, column=1, padx=5, pady=5)
#
# button_browse_output = tk.Button(root, text="Wybierz folder", command=select_output_folder)
# button_browse_output.grid(row=1, column=2, padx=5, pady=5)
#
# # Przyciski do konwersji i wyjścia
# button_convert = tk.Button(root, text="Konwertuj",
#                            command=lambda: resize_and_convert_to_gray(listbox_input.get(0, tk.END),
#                                                                       entry_output.get()))
# button_convert.grid(row=2, column=1, pady=10)
#
# button_exit = tk.Button(root, text="Wyjdź", command=root.destroy)
# button_exit.grid(row=3, column=1, pady=10)
#
# # Uruchomienie głównej pętli Tkinter
# root.mainloop()
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox


def zapisz_do_pliku(dane, nazwa_pliku):
    with open(nazwa_pliku, 'w') as plik:
        for wiersz in dane:
            plik.write(wiersz + '\n')


def resize_and_convert_to_gray(input_paths, output_folder):
    for input_path in input_paths:
        try:
            # Wczytanie obrazu
            original_image = cv2.imread(input_path)
            if original_image is None:
                messagebox.showerror("Błąd", "Nie można wczytać pliku: {}".format(input_path))
                continue

            # Zmiana rozmiaru na 32x16
            resized_image_32x16 = cv2.resize(original_image, (32, 16))

            # Konwersja obrazu na skalę szarości
            gray_image_32x16 = cv2.cvtColor(resized_image_32x16, cv2.COLOR_BGR2GRAY)

            # Pobranie nazwy pliku bez ścieżki
            filename = input_path.split("/")[-1]

            # Zapis obrazu do pliku
            cv2.imwrite(output_folder + "/{}_32x16.jpg".format(filename), gray_image_32x16)

            # Zapisanie macierzy jako pliku tekstowego
            np.savetxt(output_folder + "/{}_32x16_matrix.txt".format(filename), gray_image_32x16, fmt='%d',
                       delimiter=',', newline='\n')

            # Dodanie "[[" na początku pliku
            dane = ["[["]

            # Wstawienie "], [" po każdych 31 przecinkach
            for i in range(16):
                wiersz = ",".join(map(str, gray_image_32x16[i]))
                dane.append(wiersz)
                if i < 15:
                    dane.append("], [")

            # Dodanie "]]" na końcu pliku
            dane.append("]]")

            # Zapisanie danych do pliku tekstowego
            zapisz_do_pliku(dane, output_folder + "/{}_32x16_matrix.txt".format(filename))

        except Exception as e:
            messagebox.showerror("Błąd", "Wystąpił błąd podczas przetwarzania pliku: {}\n{}".format(input_path, str(e)))
    messagebox.showinfo("Informacja", "Konwersja zakończona pomyślnie.")



def select_input_files():
    input_paths = filedialog.askopenfilenames(title="Wybierz pliki wejściowe")
    for input_path in input_paths:
        listbox_input.insert(tk.END, input_path)


def select_output_folder():
    output_folder = filedialog.askdirectory(title="Wybierz folder wyjściowy")
    entry_output.delete(0, tk.END)
    entry_output.insert(0, output_folder)


# Tworzenie głównego okna Tkinter
root = tk.Tk()
root.title("Konwersja obrazów")

# Etykiety i pola do wprowadzania ścieżek
label_input = tk.Label(root, text="Wybrane pliki wejściowe:")
label_input.grid(row=0, column=0, padx=5, pady=5, sticky="w")

listbox_input = tk.Listbox(root, width=50, height=10)
listbox_input.grid(row=0, column=1, padx=5, pady=5)

button_browse_input = tk.Button(root, text="Wybierz pliki", command=select_input_files)
button_browse_input.grid(row=0, column=2, padx=5, pady=5)

label_output = tk.Label(root, text="Folder wyjściowy:")
label_output.grid(row=1, column=0, padx=5, pady=5, sticky="w")

entry_output = tk.Entry(root, width=50)
entry_output.grid(row=1, column=1, padx=5, pady=5)

button_browse_output = tk.Button(root, text="Wybierz folder", command=select_output_folder)
button_browse_output.grid(row=1, column=2, padx=5, pady=5)

# Przyciski do konwersji, wyjścia i wyjścia
button_convert = tk.Button(root, text="Konwertuj",
                           command=lambda: [resize_and_convert_to_gray(listbox_input.get(0, tk.END),
                                                                       entry_output.get()), root.destroy()])
button_convert.grid(row=2, column=1, pady=10)

button_exit = tk.Button(root, text="Wyjdź", command=root.destroy)
button_exit.grid(row=3, column=1, pady=10)

# Uruchomienie głównej pętli Tkinter
root.mainloop()


