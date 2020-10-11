import numpy as np
import cv2
import dlib
import os
from PIL import ImageFont, ImageDraw, Image

# 정의한 함수들
import data
import mask
import mouth

# face detector와 landmark predictor 정의
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 비디오 읽어오기
video_path = 'video/video_eng0.mp4'
cap = cv2.VideoCapture(video_path)
# 자막 읽어오기
data = data.makefile("sentence/video_eng0_sentence.csv")  # 읽어올 파일

# 자막 준비
text = ""
font = ImageFont.truetype("fonts/gulim.ttf", 20)

# 영상 저장 준비
out = mask.save_video(video_path, cap)

# 초당 프레임 수
fps = int(cap.get(cv2.CAP_PROP_FPS))

# 각 frame마다 얼굴 찾고, landmark 찍기
while True:
    ret, frame = cap.read()
    if not ret:
        break
    resized = frame

    # 현재 프레임 수
    count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    print(count)

    # 얼굴 detection
    rects = detector(resized, 1)

    for i, rect in enumerate(rects):
        # 찾은 얼굴의 박스좌표
        l = rect.left()
        t = rect.top()
        b = rect.bottom()
        r = rect.right()

        # 말풍선 위치할 좌표
        x = int(l-0.5*(r-l))
        y = int(t+1.2*(b-t))
        w = int(2.3*(r-l))  # int(2.3*(r-l))
        h = int(1.3*(b-t))  # int(1.3*(b - t))

        # 자막 위치할 좌표
        word_x = int(x + (w * 0.05))
        word_y = int(y + (h * 0.25))

        # 말풍선 가져오기
        face_mask = cv2.imread('word2.png')

        # 자막 처리
        mask_image = Image.fromarray(face_mask)
        draw = ImageDraw.Draw(mask_image)

        # facial landmark 찾기
        shape = predictor(resized, rect)
        # 입 움직임 비율 구하기
        ratio = mouth.search_mouth(shape, resized)

        # facial landmark를 빨간색 점으로 찍어서 표현 (얼굴 인식 확인용)
        for j in range(68):
            red_x, red_y = shape.part(j).x, shape.part(j).y
            cv2.circle(resized, (red_x, red_y), 1, (0, 0, 255), -1)

        # 말하고 있는지 판별하기
        if (ratio < 50 and ratio > 3):  # 말하고 있으면
            if(ratio >= 38 and ratio <= 42):  # 강경화 영상에서 말하지 않으면
                ratio = ratio
            elif (ratio > 26 and ratio <= 29):  # 트럼프 영상에서 말하지 않으면
                ratio = ratio
            else:       # 나름 정확한 말하고 있으면
                # re_ratio = str(round(ratio, 2)) #정확할 때 ratio값 소수점 두째자리까지 저장

                # 자막 넣기
                num = len(data)
                for n in range(0, num):
                    # 자막이 해당 시간안에 들어오는지 터미널로 확인
                    print("-------------------------")
                    print(int(float(data['start'][n])) * fps)
                    print(count)
                    print(int(float(data['end'][n])) * fps)
                    print("-------------------------")
                    # 자막이 해당 시간안에 들어오면
                    if int(float(data['start'][n]))*fps <= count & count < int(float(data['end'][n]))*fps:
                        text = data['textSplit'][n]
                        draw.text((30, 40), text, font=font,
                                  fill=(0, 0, 0))
                        face_mask = np.array(mask_image)
                    print("*************************")
                # 말풍선 이미지 합성하기
                resized = mask.makemask(face_mask, resized, x, y, w, h)
        # 처리된 이미지 보여주기
        cv2.imshow('frame', resized)
        # 영상으로 저장
        out.write(resized)
        #count =+ 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
