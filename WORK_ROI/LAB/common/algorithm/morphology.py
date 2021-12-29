"""
Created by SungMin Yoon on 2021-10-21..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""

import cv2
import numpy as np

DST_MORPHOLOGY = None


def processing(img_src):
    print('morphology.py')

    global DST_MORPHOLOGY

    # 구조화 요소 커널, 사각형 (3x3) 생성
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # 침식 연산 적용
    erosion = cv2.erode(img_src, k)

    # 결과 출력
    DST_MORPHOLOGY = np.hstack((img_src, erosion))

    return DST_MORPHOLOGY
