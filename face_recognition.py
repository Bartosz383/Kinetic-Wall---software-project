import numpy as np
import cv2

haar_cascade = cv2.CascadeClassifier('haar_face.xml')

people = ['Ben Afflek', 'Elton John', 'Jerry Seinfield', 'Madonna', 'Mindy Kaling']
features = np.load('features.npy', allow_pickle=True)
labels = np.load('labels.npy')

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')

img = cv2.imread(r'D:\Repozytoria i inne takie\KineticWall\Kinetic-Wall---software-project\Faces\val\jerry_seinfeld\2.jpg', cv2.IMREAD_GRAYSCALE)

# Wykryj twarze na obrazie przy użyciu kaskady Haara
faces_rect = haar_cascade.detectMultiScale(img, 1.1, 4)

# Konwersja z odcieni szarości na obraz kolorowy (RGB)
img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

# Iteruj po każdej znalezionej twarzy
for (x, y, w, h) in faces_rect:
    # Wybierz obszar zainteresowania (ROI) - fragment obrazu zawierający twarz
    faces_roi = img[y:y+h, x:x+h]

    # Przewiduj etykietę i pewność dla danego obszaru twarzy
    # Wyświetl etykietę i pewność w konsoli
    label, confidence =  face_recognizer.predict(faces_roi)
    print(f'Label = {people[label]} with a confidence of {confidence}')

    # Dodaj tekst z etykietą nad znalezioną twarzą
    cv2.putText(img_rgb, str(people[label]), (20, 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), thickness=2)

    # Dodaj prostokąt wokół znalezionej twarzy
    cv2.rectangle(img_rgb, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)

# Wyświetl obraz z zaznaczonymi twarzami
cv2.imshow('Detected Face', img_rgb)

# Czekaj na naciśnięcie dowolnego klawisza
cv2.waitKey(0)
