import cv2
import tkinter as tk
from Wyswietlacz import DisplayWindow
import time

def initialize_cascade():
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    if face_cascade.empty():
        print("Error loading face cascade.")
        exit()

    return face_cascade

def initialize_camera():
    video = cv2.VideoCapture(0)

    if not video.isOpened():
        print("Error opening video stream.")
        exit()

    return video

def detect_faces(frame, face_cascade, display_window):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        for x, y, w, h in faces:
            img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            print("Jest twarz na zdjęciu")

        # Wywołaj funkcję wall_function z opóźnieniem
        display_window.after(1000, wall_function, display_window)

    return frame

def wall_function(display_window):
    # Wywołaj funkcję Freelab_text po upływie 4 sekund
    display_window.Freelab_text()

def process_video(video, face_cascade, display_window):
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
    display_window.after(1, process_video, video, face_cascade, display_window)

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
