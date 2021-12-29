"""
Created by SungMin Yoon on 2021-02-08..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2


# 템플릿 알고리즘
def template(cv_image, img_trim):
    rectangle_list = []
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    for meth in methods:
        method = eval(meth)

        res = cv2.matchTemplate(cv_image, img_trim, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        rectangle_list.append([top_left[0], top_left[1]])

    return rectangle_list



