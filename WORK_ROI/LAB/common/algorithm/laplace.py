"""
Created by SungMin Yoon on 2021-09-08..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import cv2

DST_LAPLACE = None


def processing(img_src):
    print('Laplace.py')

    global DST_LAPLACE

    img_la = cv2.Laplacian(img_src, -1)
    DST_LAPLACE = cv2.addWeighted(img_src, 1.5, img_la, -0.5, 0)

    return DST_LAPLACE
