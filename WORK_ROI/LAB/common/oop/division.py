"""
Created by SungMin Yoon on 2021-02-08..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import math

from LAB.common.model.roi import Roi
from LAB.common.util import img_empty


class Division:

    def __init__(self):
        pass

    @classmethod
    def half(cls, roi_mask):

        user = Roi()
        user.set_mask(roi_mask)

        # 마스크 이미지
        mask = user.image_mask

        # 반올림 형변환
        f_value = float(user.rect_width / 2)
        int_math = math.floor(f_value)

        # 왼쪽 잘라내기
        left_mask = mask[user.rect_start_y:user.rect_start_y + user.rect_height,
                    user.rect_start_x:user.rect_start_x + int_math]

        # 오른쪽 잘라내기
        right_mask = mask[user.rect_start_y:user.rect_start_y + user.rect_height,
                     user.rect_start_x + int_math:user.rect_start_x + user.rect_width]

        # 크기다른 이미지 붙여넣기
        # 왼쪽, 오른쪽 마스크 나누기
        left_img = img_empty.cv_add(user.image_size_x,
                                    user.image_size_y,
                                    user.rect_start_x,
                                    user.rect_start_y,
                                  left_mask)

        right_img = img_empty.cv_add(user.image_size_x,
                                     user.image_size_y,
                                     user.rect_start_x + int_math,
                                     user.rect_start_y,
                                    right_mask)

        # set_index = f'fix'
        # cv.imshow(set_index, mask)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        return left_img, right_img





