import tkinter as tk
from Obraz_Na_Zwyo import Application
from Image_To_Frame_Tool import ImageConverterApp

def Obraz_Na_Zywo_App():
    # Utwórz nowe okno dla aplikacji
    new_window = tk.Toplevel(root)
    new_window.title("Narzędzie do transmisji obrazu")

    # Zainicjuj aplikację w nowym oknie
    app = Application(new_window)
def Obraz_Na_Ramke_App():
    app = ImageConverterApp()

# Tworzenie głównego okna
root = tk.Tk()
root.title("Kinetic Wall")

# Tworzenie etykiety
label = tk.Label(root, text="Wybierz narzędzie")
label.pack(pady=10)

# Tworzenie przycisku
button = tk.Button(root, text="Transmisja obrazu na żywo", command=Obraz_Na_Zywo_App)
button.pack(pady=5)

button = tk.Button(root, text="Konwersja zdjęcia na ramkę", command=Obraz_Na_Ramke_App)
button.pack(pady=5)

# Uruchomienie pętli głównej
root.mainloop()
