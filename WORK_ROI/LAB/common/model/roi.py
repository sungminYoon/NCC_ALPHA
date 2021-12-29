"""
Created by SungMin Yoon on 2020-10-13..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import math
from LAB.common.util import img_helper


class Roi:
    image_cv = None
    image_mask = None
    image_size_x = None
    image_size_y = None

    position_list = None

    rect_level = 0          # 레벨 저장
    rect_dimensions = 0     # 넓이
    rect_center_x = 0       # 중심 좌표 x
    rect_center_y = 0       # 중심 좌표 y
    rect_start_x = 0        # 시작 좌표 x
    rect_start_y = 0        # 시작 좌표 y
    rect_width = 0          # 가로 길이
    rect_height = 0         # 세로 길이

    def set_mask(self, mask):
        mask_h, mask_w = mask[:2]
        x, y, w, h = img_helper.square(mask)
        self.image_mask = mask
        self.image_size_x = mask_w
        self.image_size_y = mask_h
        self.rect_start_x = x
        self.rect_start_y = y
        self.rect_width = w
        self.rect_height = h
        self.dimensions()
        self.center()
        self.create_cnt(mask)

    # roi 중심값
    def center(self):
        self.rect_center_x = math.floor(self.rect_start_x + (self.rect_width / 2))
        self.rect_center_y = math.floor(self.rect_start_y + (self.rect_height / 2))

    # roi 넓이
    def dimensions(self):
        self.rect_dimensions = self.rect_width * self.rect_height

    # roi 좌표 리스트
    def create_cnt(self, mask):
        self.position_list = img_helper.mask_to_position(mask)
