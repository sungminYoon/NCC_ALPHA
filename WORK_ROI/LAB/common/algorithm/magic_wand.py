"""
Created by SungMin Yoon on 2020-06-03..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv
import numpy as np

CONNECTIVITY = 4        # 연결성


# 마스크 이미지 쓰레숄드
def get_threshold(threshold, img, x, y):

    height, width = img.shape
    flood_mask = np.zeros((height + 2, width + 2), np.uint8)
    flood_fill_flags = (CONNECTIVITY | cv.FLOODFILL_FIXED_RANGE | cv.FLOODFILL_MASK_ONLY | 255 << 8)

    cv.floodFill(img, flood_mask, (x, y), 0,
                 threshold,
                 threshold,
                 flood_fill_flags)
    flood_mask = flood_mask[1:-1, 1:-1].copy()
    return flood_mask





