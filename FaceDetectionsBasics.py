import cv2
import mediapipe as mp
import time

def detect_faces(img, face_detection):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detection.process(imgRGB)

    if results.detections:
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(img, bbox, (255, 0, 255), 2)
            cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                        (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                        2, (255, 0, 255), 2)
    return img

def calculate_fps(prev_time):
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    return fps, current_time

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0

    mpFaceDetection = mp.solutions.face_detection
    faceDetection = mpFaceDetection.FaceDetection(0.75)

    while True:
        success, img = cap.read()

        if not success:
            print("Failed to read from camera")
            break

        img = detect_faces(img, faceDetection)

        fps, pTime = calculate_fps(pTime)

        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 0), 2)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
