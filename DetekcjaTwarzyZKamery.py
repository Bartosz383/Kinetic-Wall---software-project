import cv2
from Wyswietlacz import DisplayWindow
import Object_tracking
from Object_tracking import pattern
import random

def wall_function(display_window, x, y):
    """
    Losuje i wykonuje jedną z funkcji z listy.
    """
    list_of_functions = [
        # display_window.set_all_segments_to_zero,
        # display_window.set_all_segments_to_one,
        # display_window.set_segments_to_pattern,
        # display_window.animate_wave,
        # display_window.animate_double_wave,
        # display_window.Freelab_text,
        # display_window.shift_down,
        # display_window.shift_up,
        # display_window.shift_left,
        # display_window.shift_right,
        # display_window.animate,
        # display_window.animate_loop,
        # display_window.Module_0_On,
        display_window.zmien_modul  # I noticed you're already using this one
    ]

    random_function = random.choice(list_of_functions)

    # Call the function with appropriate parameters
    if random_function == display_window.zmien_modul:
        random_function(x, y)
    else:
        random_function()


def initialize_cascade():
    """
    Inicjalizuje kaskadę do detekcji twarzy.
    """
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    if face_cascade.empty():
        print("Error loading face cascade.")
        exit()

    return face_cascade

def initialize_camera():
    """
    Inicjalizuje kamerę.
    """
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Error opening video stream.")
        exit()

    # Pobierz rozmiar klatki
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Rozmiar klatki: {frame_width}x{frame_height}")

    return video


def detect_faces(frame, face_cascade, display_window):
    """
    Detekuje twarze na obrazie i wywołuje wall_function z opóźnieniem.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        for x, y, w, h in faces:
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # Przekształć współrzędne
            transformed_x, transformed_y = transform_coordinates(x, y)

            print(f"Twarz na przekształconej pozycji X: {transformed_x}, Y: {transformed_y}")

            # Wywołaj funkcję wall_function z przekształonymi współrzędnymi
            display_window.after(10, wall_function, display_window, transformed_x, transformed_y)

    return frame

def transform_coordinates(x, y):
    """
    Przekształca współrzędne x i y z zakresu 0-640 i 0-480 na zakres 0-28 i 0-12.
    """
    transformed_x = (x / 640) * 28
    transformed_y = (y / 480) * 12
    return transformed_x, transformed_y

def process_video(video, face_cascade, display_window):
    """
    Przetwarza strumień wideo i wyświetla obrazy z detekcją twarzy.
    """
    check, frame = video.read()

    if not check:
        print("Error reading video frame.")
        return

    frame_with_faces = detect_faces(frame, face_cascade, display_window)

    cv2.imshow("Detected Faces", frame_with_faces)
    key = cv2.waitKey(10)

    if key == ord('q'):
        return

    # Cykliczne sprawdzanie klatek z użyciem after
    display_window.after(1000, process_video, video, face_cascade, display_window)

def main_detect():
    face_cascade = initialize_cascade()
    video = initialize_camera()

    # Utwórz obiekt DisplayWindow
    wyswietlacz = DisplayWindow("Moje Okno")

    # Wywołaj funkcję process_video, aby rozpocząć cykliczne przetwarzanie wideo
    wyswietlacz.after(10, process_video, video, face_cascade, wyswietlacz)

    wyswietlacz.mainloop()

if __name__ == "__main__":
    main_detect()
