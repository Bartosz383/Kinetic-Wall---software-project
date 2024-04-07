import cv2

# Wczytaj obrazek
image = cv2.imread('obrazek.png', cv2.IMREAD_GRAYSCALE)

# Przekształć macierz na listę list, gdzie każdy wiersz jest osobną listą
image_lists = [list(row) for row in image]

# Wyświetl listę list
for row in image_lists:
    print(row)
