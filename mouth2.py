# mouth.search_mouth()로 호출
# shape : facial landmark 찾기

import cv2
import numpy as np
from math import *

def make_shape(shape):
    coordinates = np.zeros((68, 2), dtype=int)
    for i in range(0, 68):
        coordinates[i] = (shape.part(i).x, shape.part(i).y)
    # return the list of (x, y)-coordinates
    return coordinates


def search_mouth(shape, resized, index):

   # 얼굴 범위 리스트 설정 
    MOUTH_INNER = list(range(61, 68))

    # 입술 각 지점의 y값을 저장하기 위한 list 변수
    height = []
    # 입술 각 지점의 x값을 저장하기 위한 list 변수
    weight = []
    #얼굴들의 입술 포인트들을 저장하는 리스트
    lippoint = []

    # loop over the facial landmark regions individually
    for name in enumerate(MOUTH_INNER):
        # grab the (x, y)-coordinates associated with the
        # face landmark
        (j, k) = MOUTH_INNER[name]
        pts = shape[j:k]
        for ps in pts:
            height.append(ps[1])
            weight.append(ps[0])

        #입술 정보가 기존에 등록된 정보면 해당 index값으로 가서 값 변경
        if len(lippoint) > index:
            lippoint[index] = pts
        #새로운 입술정보가 입력됬을 때 lippoint에 추가
        else:
            lippoint.append(pts)
 
    return ratio
