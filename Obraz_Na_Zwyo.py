import numpy as np
import cv2

class YourClassName:
    def __init__(self):
        self.segments = None
        self.hex_size = None

    def Module_binary(self, normalized_matrix):
        self.segments = self.generate_segment_vectors(normalized_matrix)
        self.show_display(self.segments)

    def generate_segment_vectors(self, pattern):
        segment_vectors = []
        for i in range(4):
            for j in range(8):
                segment_name = f"segment_{i * 8 + j}"
                segment = self.create_segment_vector(pattern, i * 4, (i + 1) * 4, j * 4, (j + 1) * 4)
                segment_vectors.append((segment_name, segment))
        return segment_vectors

    def create_segment_vector(self, pattern, start_i, end_i, start_j, end_j):
        segment = []
        for i in range(start_i, end_i):
            for j in range(start_j, end_j):
                segment.append(pattern[i][j])
        return segment

    def show_display(self, segments):
        if segments is not None:
            for segment_name, segment in segments:
                print(f"{segment_name}: {segment}")
            print("\n")


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

    # Przeskalowana macierz normalized
    s_binary = cv2.resize(normalized, (320, 160))

    # Wywołaj funkcję macierz normalized
    your_object = YourClassName()
    your_object.Module_binary(normalized)

    # Wyświetl przekształcony obraz
    cv2.imshow('Processed Image', normalized)
    cv2.imshow('Scaled Processed Image', s_binary)
    cv2.imshow('Original Image', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
