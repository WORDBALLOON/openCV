import dlib
import skvideo.io
import cv2
import datetime
import numpy as np

# face detector와 landmark predictor 정의
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 비디오 읽어오기
cap = skvideo.io.vreader('video/video_eng1.mp4')

# 말풍선 가져오기
face_mask = cv2.imread('word.png')
h_mask, w_mask = face_mask.shape[:2]

# 얼굴 범위 리스트 설정
ALL = list(range(0, 68))
RIGHT_EYEBROW = list(range(17, 22))
LEFT_EYEBROW = list(range(22, 27))
RIGHT_EYE = list(range(36, 42))
LEFT_EYE = list(range(42, 48))
NOSE = list(range(27, 36))
MOUTH_OUTLINE = list(range(48, 61))
MOUTH_INNER = list(range(61, 68))
JAWLINE = list(range(0, 17))
MOUTH_INNER_TOP = list()

# 각 frame마다 얼굴 찾고, landmark 찍기
for frame in cap:
    # RGB에서 BGR로 바꾸기
    img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # 얼굴 detection
    rects = detector(img, 1)
    for i, rect in enumerate(rects):
        # 찾은 얼굴의 박스좌표
        l = rect.left()
        t = rect.top()
        b = rect.bottom()
        r = rect.right()
        # facial landmark 찾기
        shape = predictor(img, rect)
        # facial landmark를 빨간색 점으로 찍어서 표현
        for j in range(68):
            x, y = shape.part(j).x, shape.part(j).y
            cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
        # 얼굴이 있는 부분을 박스쳐주기
        cv2.rectangle(img, (l, t), (r, b), (0, 255, 0), 2)

        # MOUTH_INNER 값 확인
        print("******"+(int(MOUTH_INNER[1])-int(MOUTH_INNER[3])))
        # 처리된 이미지 보여주기
        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
