import dlib
import skvideo.io
import cv2
import mask
import mouth

# face detector와 landmark predictor 정의
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 비디오 읽어오기
video_path = 'video/example.avi'
cap = cv2.VideoCapture(video_path)

# 영상 저장 준비
out = mask.save_video(video_path, cap)

# 얼굴 범위 리스트 설정
MOUTH_OUTLINE = list(range(48, 61))
MOUTH_INNER = list(range(61, 68))
JAWLINE = list(range(0, 17))
MOUTH_INNER_TOP = list()

# 각 frame마다 얼굴 찾고, landmark 찍기
while True:
    ret, frame = cap.read()
    if not ret:
        break
    resized = frame

    # 얼굴 detection
    rects = detector(resized, 1)

    for i, rect in enumerate(rects):
        l = rect.left()
        t = rect.top()
        b = rect.bottom()
        r = rect.right()
        # facial landmark 찾기
        shape = predictor(resized, rect)
        # 입 움직임 비율 구하기
        ratio = mouth.search_mouth(shape, resized)

        # facial landmark를 빨간색 점으로 찍어서 표현 (얼굴 인식 확인용)
        for j in range(68):
            red_x, red_y = shape.part(j).x, shape.part(j).y
            cv2.circle(resized, (red_x, red_y), 1, (0, 0, 255), -1)

        cv2.rectangle(resized, (l, t), (r, b), (0, 255, 0), 2)
        cv2.putText(resized, str(round(ratio, 2)),
                    (l, b+30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0))
        cv2.imshow('frame', resized)
        out.write(resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
