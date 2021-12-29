"""
Created by SungMin Yoon on 2021-02-24..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv
import numpy as np


# 이미지 윈도우 레벨 (minimum_unit = 0.1 ~ 0.9 최소 단위 레벨링)
def get_level(img_data, window, level, minimum_unit):
    result = np.piecewise(img_data,
                          [img_data <= (level - minimum_unit - (window - 1) / 2),
                           img_data > (level - minimum_unit + (window - 1) / 2)],
                          [0, 255,
                           lambda data: ((data - (level - minimum_unit)) / (window - 1) + minimum_unit) * (255 - 0)])
    return result


# 연부조직
def soft_tissue(cv_image, soft_tissue_level, window, muscle, unit):
    _soft_tissue = get_level(cv_image, window, soft_tissue_level, unit)
    _muscle = get_level(cv_image, window, muscle, unit)

    # 연부조직 roi 를 만듭니다.
    rows, cols, _ = _muscle.shape
    roi = _soft_tissue[0:rows, 0:cols]

    # 역방향 마스크를 만듭니다.
    ret, mask = cv.threshold(_muscle, 10, 0, cv.THRESH_BINARY)
    mask_inv = cv.bitwise_not(mask)

    # roi 영역 까맣게 만들어 줍니다.
    img1_bg = cv.bitwise_not(roi, roi, mask=mask_inv)

    # 이미지 에서 roi 영역만 가지고 옵니다.
    img2_fg = cv.bitwise_and(_muscle, _muscle, mask=mask)

    # roi 를 바탕 이미지와 결합 합니다.
    dst = cv.add(img1_bg, img2_fg)
    _soft_tissue[0:rows, 0:cols] = dst

    return _soft_tissue


# 조직 레벨링
def tissue_process(cv_image, _tissue_level, window, muscle, unit):
    _tissue = get_level(cv_image, window, _tissue_level, unit)
    _muscle = get_level(cv_image, window, muscle, unit)

    # 연부조직 roi 를 만듭니다.
    rows, cols = _muscle.shape[:2]
    roi = _tissue[0:rows, 0:cols]

    # roi 를 바탕 이미지와 결합 합니다.
    dst = cv.add(roi, _muscle)
    _tissue[0:rows, 0:cols] = dst
    return _tissue
