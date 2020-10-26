import numpy as np
import cv2
import dlib
from PIL import ImageFont, ImageDraw, Image
from collections import OrderedDict
import data
import mask
import mouth2

# face detector와 landmark predictor 정의
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 비디오 읽어오기
video_path = 'video/video_self2.mp4'
cap = cv2.VideoCapture(video_path)
# 자막 읽어오기
data = data.makefile("sentence/pitapat_sentence.csv")  # 읽어올 파일
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
    resized = cv2.resize(frame, dsize=(1000, 600),
                         interpolation=cv2.INTER_AREA)

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
        x = int(l+(r-l)/2-150)
        y = int(t+1.2*(b-t))
        w = 300  # int(2.3*(r-l))
        h = 200  # int(1.3*(b - t))

        if (x < 0):  # 말풍선이 왼쪽으로 벗어날 때
            x = 0
        if (x + w > 1000):  # 말풍선이 오른쪽으로 벗어날 때
            x = 700
        if (y < -600):  # 말풍선이 아래로 벗어날 때
            y = -400

        # 자막 위치할 좌표
        word_x = int(x + (w * 0.05))
        word_y = int(y + (h * 0.25))

        # 말풍선 가져오기
        face_mask = cv2.imread('word2.png')
        # 마스크 크기 조절
        face_mask_small = cv2.resize(
            face_mask, (w, h), interpolation=cv2.INTER_AREA)
        # 자막 처리
        mask_image = Image.fromarray(face_mask_small)
        draw = ImageDraw.Draw(mask_image)

        # facial landmark 찾기
        shape = predictor(resized, rect)
        shape = mouth2.make_shape(shape)
        # 입 움직임 비율 구하기
        # ratio = mouth2.search_mouth(shape, resized, i)
        # 얼굴 범위 리스트 설정 
        MOUTH_INNER = OrderedDict([("Mouth", (48, 68)),])

        # 입술 각 지점의 y값을 저장하기 위한 list 변수
        height = []
        # 입술 각 지점의 x값을 저장하기 위한 list 변수
        weight = []
        #얼굴들의 입술 포인트들을 저장하는 리스트
        lippoint = []

        # loop over the facial landmark regions individually
        for name in enumerate(MOUTH_INNER.keys()):
            # grab the (x, y)-coordinates associated with the
            # face landmark
            (j, k) = MOUTH_INNER[name]
            pts = shape[j:k]
            for ps in pts:
                height.append(ps[1])
                weight.append(ps[0])

                #입술 정보가 기존에 등록된 정보면 해당 index값으로 가서 값 변경
                if len(lippoint) > i:
                    lippoint[index] = pts
                #새로운 입술정보가 입력됬을 때 lippoint에 추가
                else:
                    lippoint.append(pts)

        height.clear()
        weight.clear()

        #가져온 입술의 정보를 x값는 weight 리스트에, y값은 height 리스트에 저장한다.
        for point in lippoint[i]:
            height.append(point[1])
            weight.append(point[0])

        #입술안의 삼각형 각도를 구한다.
        ratio = (lippoint[i][18][1] - lippoint[i][0][1]) / (lippoint[i][18][0] - lippoint[i][0][0])




        # facial landmark를 빨간색 점으로 찍어서 표현 (얼굴 인식 확인용)
        for j in range(68):
            red_x, red_y = shape.part(j).x, shape.part(j).y
            cv2.circle(resized, (red_x, red_y), 1, (0, 0, 255), -1)
        
        x_left = 0
        x_right = 0
        num = len(data)
        for n in range(0, num):
            # 자막이 해당 시간안에 들어오는지 터미널로 확인
            print("-------------------------")
            print(int(float(data['start'][n])) * fps)
            print(count)
            print(int(float(data['end'][n])) * fps)
            print("-------------------------")
           
           

            # 자막이 해당 시간안에 들어오면
            if int(float(data['start'][n])) * fps <= count & count < int(float(data['end'][n])) * fps:
                text = data['textSplit'][n]
                draw.text((10, 30), " "+text, font=font, fill=(0, 0, 0))
                face_mask_small = np.array(mask_image)

                # 말하고 있는지 판별하기
                if (ratio > 0.25):
                    #시작시간부터 50개
                    if (count <= int(float(data['start'][n])) * fps + 30):
                        # x가 왼쪽인지 오른쪽인지 카운트
                        if x < 500 : x_left += 1
                        else : x_right += 1
                        # 말풍선 이미지 합성하기
                        resized = mask.makemask(face_mask_small, resized, x, y, w, h)
                    elif count == int(float(data['end'][n])) * fps:
                        x_left = 0
                        x_right = 0
                        # 말풍선 이미지 합성하기
                        resized = mask.makemask(face_mask_small, resized, x, y, w, h)
                    else:
                        if x_left > x_right:
                            if x < 500:
                                # 말풍선 이미지 합성하기
                                resized = mask.makemask(face_mask_small, resized, x, y, w, h)
                        else:
                            if x >= 500:
                                # 말풍선 이미지 합성하기
                                resized = mask.makemask(face_mask_small, resized, x, y, w, h)
            
        # 처리된 이미지 보여주기
        cv2.imshow('frame', resized)
        # 영상으로 저장
        out.write(resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()