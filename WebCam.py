# import cv2 as cv
#
# ### odczyt zdjęcia
#
# img = cv.imread('Photos/cat_large.jpg')
#
# cv.imshow('Cat', img)
#
# def rescaleFrame(frame, scale=0.75):
#     width = int(frame.shape[1] * scale)
#     height = int(frame.shape[0] * scale)
#     dimensions = (width, height)
#
#     return  cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
#
# cv.waitKey(0)
#
# def changeRes(width, height):
#     # Live video
#     capture.set(3, width)
#     capture.set(4, height)
#
# ## odczyt wideo
# capture = cv.VideoCapture('Videos/dog.mp4') # 0 to odniesienie do kamery w kompie
# # capture = cv.VideoCapture('0')
#
# while True:
#     isTrue, frame = capture.read()
#
#     frame_resized = rescaleFrame(frame)
#
#     cv.imshow('Video', frame)
#     cv.imshow('Video Resized', frame_resized)
#
#     if cv.waitKey(20) & 0xFF==ord('d'): # d przerywa pętle
#         break
#
# capture.release()
# cv.destroyAllWindows()

## Web Cam

# import the opencv library
# import cv2
#
# # define a video capture object
# vid = cv2.VideoCapture(0)
#
# while (True):
#
#     # Capture the video frame
#     # by frame
#     ret, frame = vid.read()
#
#     # Display the resulting frame
#     cv2.imshow('frame', frame)
#
#     # the 'q' button is set as the
#     # quitting button you may use any
#     # desired button of your choice
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # After the loop release the cap object
# vid.release()
# # Destroy all the windows
# cv2.destroyAllWindows()

import cv2
import numpy as np

# Zdefiniowanie kamery. Indeks 0 to pierwsza kamera, indeks 1 to druga podpięta do urządzenia. Możliwe że u ciebie będzie trzeba wpisać 1, 2, 3 lub inną liczbę jeżeli masz tak wiele kamer
vid = cv2.VideoCapture(0)

while True:
    # Wyświetlanie wideo klatka po klatce (u nas to leci na żywo)
    ret, frame = vid.read()

    # Nadanie wysokości i szerokości
    height, width, _ = frame.shape

    # Podzielenie klatki na trzy części w poziomie i trzy w pionie. Łącznie dziewięć kawałków, regionów
    region_height = height // 3
    region_width = width // 3

    # Określenie górnego rzędu
    top_left = frame[0:region_height, 0:region_width]
    top_middle = frame[0:region_height, region_width:2*region_width]
    top_right = frame[0:region_height, 2*region_width:3*region_width]

    # OKreślenie środkowego rzędu
    middle_left = frame[region_height:2*region_height, 0:region_width]
    middle_middle = frame[region_height:2*region_height, region_width:2*region_width]
    middle_right = frame[region_height:2*region_height, 2*region_width:3*region_width]

    # Określenie dolnego rzędu
    bottom_left = frame[2*region_height:3*region_height, 0:region_width]
    bottom_middle = frame[2*region_height:3*region_height, region_width:2*region_width]
    bottom_right = frame[2*region_height:3*region_height, 2*region_width:3*region_width]

    # Maska
    top_left_mask = np.zeros_like(top_left)
    top_middle_mask = np.zeros_like(top_middle)
    top_right_mask = np.zeros_like(top_right)

    middle_left_mask = np.zeros_like(middle_left)
    middle_middle_mask = np.zeros_like(middle_middle)
    middle_right_mask = np.zeros_like(middle_right)

    bottom_left_mask = np.zeros_like(bottom_left)
    bottom_middle_mask = np.zeros_like(bottom_middle)
    bottom_right_mask = np.zeros_like(bottom_right)

    # Dodaje każdej masce jej określony kolor
    top_left_mask[:, :] = [0, 0, 255]  # Red
    top_middle_mask[:, :] = [0, 255, 0]  # Green
    top_right_mask[:, :] = [255, 0, 0]  # Blue

    middle_left_mask[:, :] = [0, 255, 255]  # Yellow
    middle_middle_mask[:, :] = [255, 0, 255]  # Magenta
    middle_right_mask[:, :] = [255, 255, 0]  # Cyan

    bottom_left_mask[:, :] = [255, 128, 0]  # Olive
    bottom_middle_mask[:, :] = [128, 0, 255]  # Purple
    bottom_right_mask[:, :] = [128, 128, 128]  # Teal

    # Dodaje maskę do konkretnego regionu
    top_left = cv2.bitwise_and(top_left, top_left_mask)
    top_middle = cv2.bitwise_and(top_middle, top_middle_mask)
    top_right = cv2.bitwise_and(top_right, top_right_mask)

    middle_left = cv2.bitwise_and(middle_left, middle_left_mask)
    middle_middle = cv2.bitwise_and(middle_middle, middle_middle_mask)
    middle_right = cv2.bitwise_and(middle_right, middle_right_mask)

    bottom_left = cv2.bitwise_and(bottom_left, bottom_left_mask)
    bottom_middle = cv2.bitwise_and(bottom_middle, bottom_middle_mask)
    bottom_right = cv2.bitwise_and(bottom_right, bottom_right_mask)

    # Tworzę pustą kanwę
    canvas = np.zeros_like(frame)

    # Umieszczam na kanwie każdy z regionó
    canvas[0:region_height, 0:region_width] = top_left
    canvas[0:region_height, region_width:2*region_width] = top_middle
    canvas[0:region_height, 2*region_width:3*region_width] = top_right

    canvas[region_height:2*region_height, 0:region_width] = middle_left
    canvas[region_height:2*region_height, region_width:2*region_width] = middle_middle
    canvas[region_height:2*region_height, 2*region_width:3*region_width] = middle_right

    canvas[2*region_height:3*region_height, 0:region_width] = bottom_left
    canvas[2*region_height:3*region_height, region_width:2*region_width] = bottom_middle
    canvas[2*region_height:3*region_height, 2*region_width:3*region_width] = bottom_right

    # Wyświetlam kanwę
    cv2.imshow('Grouped Windows', canvas)

    # Jeżeli chcesz wyjść kliknij 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Wyświetl wideo
vid.release()
# Zamknij wszystkie okna
cv2.destroyAllWindows()

