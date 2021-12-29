"""
Created by SungMin Yoon on 2021-09-15..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import cv2

DST_CANNY = None


def processing(img_src):
    print('Canny.py')

    global DST_CANNY

    img_c = cv2.Canny(img_src, 100, 200)
    DST_CANNY = cv2.addWeighted(img_src, 1.5, img_c, -0.5, 0)

    return DST_CANNY
