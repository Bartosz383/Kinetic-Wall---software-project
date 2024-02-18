import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import time
import threading

from Wyswietlacz import DisplayWindow
from DetekcjaTwarzyZKamery import main_detect

def main():
    # Utwórz obiekt DisplayWindow
    wyswietlacz = DisplayWindow("Moje Okno")

    # Utwórz wątek dla funkcji main_detect
    detect_thread = threading.Thread(target=main_detect)

    # Uruchom wątek detekcji
    detect_thread.start()

    # Uruchom główną pętlę GUI dla wyswietlacza
    wyswietlacz.mainloop()

if __name__ == "__main__":
    main()
