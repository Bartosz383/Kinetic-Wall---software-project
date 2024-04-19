import numpy as np
import cv2
from Wyswietlacz import DisplayWindow

class YourClassName:
    def __init__(self):
        self.segments = None
        self.hex_size = None

    def Module_binary(self, binary_matrix):
        self.segments = binary_matrix
        self.show_display(self.hex_size)

    def show_display(self, size):
        if self.segments is not None:
            print(self.segments)


# Rejestruj obraz z kamery i wyświetlaj go na żywo
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Przekształć obraz na skalę szarości
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Przeskaluj obraz do rozdzielczości 32x16
    resized = cv2.resize(gray, (32, 16))

    # Dokonaj normalizacji przekształconego szarego obrazu
    normalized = resized / 255.0

    # Dla każdego piksela zmień jego kolor na czarny lub biały zgodnie z warunkiem
    binary = np.where(normalized >= 0.5, 255, 0).astype(np.uint8)

    # Przeskalowana macierz binary
    s_binary = cv2.resize(binary, (320, 160))

    # Wywołaj funkcję Module_binary, aby przekazać macierz binarną
    your_object = YourClassName()
    your_object.Module_binary(binary)

    # Wyświetl przekształcony obraz
    cv2.imshow('Processed Image', binary)
    cv2.imshow('Scaled Processed Image', s_binary)
    cv2.imshow('Original Image', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
