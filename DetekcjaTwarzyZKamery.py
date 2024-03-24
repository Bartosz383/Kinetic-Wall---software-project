import cv2
from Wyswietlacz import DisplayWindow
import random
import mediapipe as mp
import time

mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection(0.75)

def wall_function(display_window, x, y):
    """
    Losuje i wykonuje jedną z funkcji z listy.
    """
    list_of_functions = [
        display_window.zmien_modul
    ]

    random_function = random.choice(list_of_functions)

    # Call the function with appropriate parameters
    if random_function == display_window.zmien_modul:
        random_function(x, y)
    else:
        random_function()

def detect_faces(video, display_window, prev_time):
    """
    Detekuje twarze na obrazie i wywołuje wall_function z przekształconymi współrzędnymi twarzy.
    """
    check, frame = video.read()

    if not check:
        print("Error reading video frame.")
        return

    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = frame.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)

            # Rysowanie ramki wokół twarzy
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)

            # Przekształć współrzędne
            transformed_x, transformed_y = transform_coordinates(bbox[0], bbox[1])

            # Wywołaj funkcję wall_function z przekształonymi współrzędnymi
            wall_function(display_window, transformed_x, transformed_y)

    # Wyświetlenie liczby klatek na sekundę (FPS)
    fps, prev_time = calculate_fps(prev_time)
    cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (0, 255, 0), 2)

    # Wyświetlenie obrazu z ramkami i liczbą FPS
    cv2.imshow("Detected Faces", frame)

    # Cykliczne sprawdzanie klatek z użyciem after
    display_window.after(10, detect_faces, video, display_window, prev_time)

def transform_coordinates(x, y):
    """
    Przekształca współrzędne x i y z zakresu 0-640 i 0-480 na zakres 0-28 i 0-12.
    """
    transformed_x = (x / 640) * 28
    transformed_y = (y / 480) * 12
    return transformed_x, transformed_y

def calculate_fps(prev_time):
    """
    Oblicza liczbę klatek na sekundę (FPS) w kontekście przetwarzania strumienia wideo.
    """
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if current_time != prev_time else 0
    return fps, current_time

def main_detect():
    video = cv2.VideoCapture(0)

    # Utwórz obiekt DisplayWindow
    wyswietlacz = DisplayWindow("Moje Okno")

    prev_time = time.time()

    # Rozpocznij detekcję twarzy
    detect_faces(video, wyswietlacz, prev_time)

    wyswietlacz.mainloop()

if __name__ == "__main__":
    main_detect()
