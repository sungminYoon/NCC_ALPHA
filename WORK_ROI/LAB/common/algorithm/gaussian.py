"""
Created by SungMin Yoon on 2021-08-30..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import cv2

DST_GAUSSIAN = None


def processing(img_src):
    print('Gaussian.py')

    global DST_GAUSSIAN

    for sigma in range(1, 4):
        img_g = cv2.GaussianBlur(img_src, (0, 0), sigma)
        DST_GAUSSIAN = cv2.addWeighted(img_src, 1.5, img_g, -0.5, 0)

    return DST_GAUSSIAN


