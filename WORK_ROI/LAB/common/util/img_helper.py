"""
Created by SungMin Yoon on 2021-02-22..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv
import numpy as np


def square(image):
    ret, thresh = cv.threshold(image, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv.boundingRect(cnt)
    return x, y, w, h


def position_to_mask(position_list, cv_width, cv_height):
    size = (cv_width, cv_height, 1)
    mask = np.zeros(size, np.uint8)
    hull = position_list
    mask_2 = cv.drawContours(mask, [hull], 0, (255, 0, 0), cv.FILLED)
    mask = cv.add(mask, mask_2)
    return mask


def mask_to_position(mask):
    # 마스크 roi position 추출
    _, thresh = cv.threshold(mask, 0, 255, 0)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    position: list = contours[0]
    return position
