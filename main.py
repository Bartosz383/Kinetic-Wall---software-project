# import tkinter.messagebox as messagebox
# import tkinter.simpledialog as simpledialog
# import time
# import threading
#
# from Wyswietlacz import DisplayWindow
# from DetekcjaTwarzyZKamery import main_detect
#
# def main():
#     # Utwórz obiekt DisplayWindow
#     wyswietlacz = DisplayWindow("Moje Okno")
#
#     # Utwórz wątek dla funkcji main_detect
#     detect_thread = threading.Thread(target=main_detect)
#
#     # Uruchom wątek detekcji
#     detect_thread.start()
#
#     # Uruchom główną pętlę GUI dla wyswietlacza
#     wyswietlacz.mainloop()
#
# if __name__ == "__main__":
#     main()

import tkinter as tk
from Obraz_Na_Zwyo import Application

def on_button_click():
    # Utwórz nowe okno dla aplikacji
    new_window = tk.Toplevel(root)
    new_window.title("Narzędzie do transmisji obrazu")

    # Zainicjuj aplikację w nowym oknie
    app = Application(new_window)

# Tworzenie głównego okna
root = tk.Tk()
root.title("Kinetic Wall")

# Tworzenie etykiety
label = tk.Label(root, text="Wybierz narzędzie")
label.pack(pady=10)

# Tworzenie przycisku
button = tk.Button(root, text="Transmisja obrazu na żywo", command=on_button_click)
button.pack(pady=5)

# Uruchomienie pętli głównej
root.mainloop()
