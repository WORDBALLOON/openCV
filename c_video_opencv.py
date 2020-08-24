import cv2
import datetime
import numpy as np

face_cascade = cv2.CascadeClassifier(
    'cascade_files/haarcascade_frontalface_alt.xml')

face_mask = cv2.imread('word.png')
h_mask, w_mask = face_mask.shape[:2]

if face_cascade.empty():
    raise IOError('Unable to load the face cascade classifier xml file')

cap = cv2.VideoCapture('video/video_eng00.mp4')
scaling_factor = 0.5


while True:
    ret, framed = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(framed, cv2.COLOR_BGR2GRAY)

    face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in face_rects:
        if h > 0 and w > 0:
            x = int(x + 0.6*w)
            y = int(y - 0.2*h)
            w = int(0.8 * 2.5*w)
            h = int(0.7 * 2*h)
            # frame 얼굴에 맞춰서 자르기
            frame_roi = framed[y:y+h, x:x+w]
            # 마스크의 크기 조절
            face_mask_small = cv2.resize(
                face_mask, (w, h), interpolation=cv2.INTER_AREA)
            # 그레이마스크
            gray_mask = cv2.cvtColor(face_mask_small, cv2.COLOR_BGR2GRAY)
            # 바탕이 검은색인 마스크를 만듦
            ret, mask = cv2.threshold(
                gray_mask, 240, 255, cv2.THRESH_BINARY_INV)
            mask_inv = cv2.bitwise_not(mask)
            masked_face = cv2.bitwise_and(
                face_mask_small, face_mask_small, mask=mask)
            masked_frame = cv2.bitwise_and(frame_roi, frame_roi, mask=mask_inv)
            framed[y:y+h, x:x+w] = cv2.add(masked_face, masked_frame)
            cv2.imshow('Face mask_inv', mask_inv)
            cv2.imshow(' masked_face', masked_face)

    cv2.imshow('Face Detector', framed)

    c = cv2.waitKey(1)
    if c == 27:
        break

# 동영상프로세싱
capture = cv2.VideoCapture("video/video_eng1.mp4")
width = int(capture.get(3))  # 가로
height = int(capture.get(4))  # 세로값 가져와서
while (capture.isOpened):
    ret, frame = capture.read()
    if ret == False:
        break
    cv2.imshow("VideoFrame", frame)
    now = datetime.datetime.now().strftime("%d_%H-%M-%S")
    key = cv2.waitKey(33)  # 1) & 0xFF
    if key == 27:  # esc 종료
        break
    elif key == 26:  # ctrl + z
        cv2.IMREAD_UNCHANGED
cv2.imwrite("cap" + ".png", frame)
cap.release()
cv2.destroyAllWindows()
