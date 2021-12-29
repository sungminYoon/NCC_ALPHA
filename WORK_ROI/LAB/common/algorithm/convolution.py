"""
Created by SungMin Yoon on 2021-09-15..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import cv2
import numpy as np

DST_CONVOLUTION = None


def processing(img_src):
    print('Convolution .py')

    global DST_CONVOLUTION

    kernel3 = np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]])
    DST_CONVOLUTION = cv2.filter2D(src=img_src, ddepth=-1, kernel=kernel3)

    return DST_CONVOLUTION
