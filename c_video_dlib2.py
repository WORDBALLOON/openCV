import dlib
import skvideo.io
import cv2
import datetime
import numpy as np
from math import *

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

# 특징점끼리 선 잇기..?


def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


# 각 frame마다 얼굴 찾고, landmark 찍기
for frame in cap:
    # RGB에서 BGR로 바꾸기
    img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # resize할 비율 구하기
    r = 200. / img.shape[1]
    dim = (200, int(img.shape[0] * r))
    # resize 하기
    #resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    # resize 하면 인식이 잘 안됨 / resize 안하면 처리속도 느림
    resized = img

    # 얼굴 detection
    rects = detector(img, 1)

    # ex_x = 10

    for i, rect in enumerate(rects):
        # 찾은 얼굴의 박스좌표
        l = rect.left()
        t = rect.top()
        b = rect.bottom()
        r = rect.right()
        # facial landmark 찾기
        shape = predictor(resized, rect)

        # 입 움직임 비율 구하기
        left_point = (shape.part(
            MOUTH_OUTLINE[12]).x, shape.part(MOUTH_OUTLINE[12]).y)
        right_point = (shape.part(
            MOUTH_INNER[3]).x, shape.part(MOUTH_INNER[3]).y)
        center_top = midpoint(shape.part(
            MOUTH_INNER[0]), shape.part(MOUTH_INNER[1]))
        center_bottom = midpoint(shape.part(
            MOUTH_INNER[5]), shape.part(MOUTH_INNER[6]))
        hor_line = cv2.line(resized, left_point, right_point, (0, 255, 0), 2)
        ver_line = cv2.line(resized, center_top, center_bottom, (0, 255, 0), 2)
        hor_line_lenght = hypot(
            (left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_lenght = hypot(
            (center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
        # 입을 벌릴수록 ratio 값 작아짐
        # 입 다물고있지 않으면 (말하고 있으면)
        if ver_line_lenght != 0:
            ratio = hor_line_lenght / ver_line_lenght
        else:
            ratio = 60

        print(ratio)

        # facial landmark를 빨간색 점으로 찍어서 표현
        for j in range(68):
            x, y = shape.part(j).x, shape.part(j).y
            cv2.circle(resized, (x, y), 1, (0, 0, 255), -1)

        # 얼굴이 있는 부분을 박스쳐주기
        if ratio < 50:  # 말하고 있으면
            # if abs(ratio-ex_ratio) < 15:   # 이전 값과 차이가 크지않다면
            cv2.rectangle(resized, (l, t), (r, b), (0, 255, 0), 2)
            # ex_ratio = ratio

        # 처리된 이미지 보여주기
        cv2.imshow('frame', resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
