import cv2


def resize_and_convert_to_gray(image_path, output_path_32x16, output_path_320x160):
    # Wczytanie obrazu
    original_image = cv2.imread(image_path)

    # Zmiana rozmiaru na 32x16
    resized_image_32x16 = cv2.resize(original_image, (32, 16))

    # Zmiana rozmiaru na 320x160
    resized_image_320x160 = cv2.resize(original_image, (320, 160))

    # Konwersja obrazów na skalę szarości
    gray_image_32x16 = cv2.cvtColor(resized_image_32x16, cv2.COLOR_BGR2GRAY)
    gray_image_320x160 = cv2.cvtColor(resized_image_320x160, cv2.COLOR_BGR2GRAY)

    # Zapis obrazów do plików
    cv2.imwrite(output_path_32x16, gray_image_32x16)
    cv2.imwrite(output_path_320x160, gray_image_320x160)


# Przykładowe użycie
input_image_path = "D:\Repozytoria i inne takie\KineticWall\Kinetic-Wall---software-project\input.jpg"  # ścieżka wejściowa
output_image_path_32x16 = "D:\Repozytoria i inne takie\KineticWall\Kinetic-Wall---software-project\output_image32x16.jpg"  # ścieżka wyjściowa 32x16
output_image_path_320x160 = "D:\Repozytoria i inne takie\KineticWall\Kinetic-Wall---software-project\output_image32x16.jpg" # 320x160

resize_and_convert_to_gray(input_image_path, output_image_path_32x16, output_image_path_320x160)
print("Konwersja zakończona pomyślnie.")
