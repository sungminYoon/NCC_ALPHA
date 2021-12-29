"""
Created by SungMin Yoon on 2021-08-30..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
from LAB.config import setting
from LAB.common.algorithm import gaussian
from LAB.common.algorithm import laplace
from LAB.common.algorithm import convolution
from LAB.common.algorithm import canny


RESULT_IMG = None


class Filter:

    # 필터 처리를 완료한 이미지 리스트 입니다.
    filtering_img_list = None
    save_img_list = None

    def __init__(self):
        print('Filter: init')
        self.filtering_img_list = []

    def choice(self, idx, img_list):
        print('Filter: choice')
        global RESULT_IMG

        self.filtering_img_list.clear()

        # 필터 처리를 합니다.
        for i in range(0, len(img_list)):

            # 필터 처리
            img = img_list[i]

            if 'Normal' is setting.FILTER[idx]:
                # 처음 받은 이미지 리스트를 리턴 합니다.
                return self.save_img_list

            if 'Gaussian' is setting.FILTER[idx]:
                RESULT_IMG = gaussian.processing(img)

            if 'Laplace' is setting.FILTER[idx]:
                RESULT_IMG = laplace.processing(img)

            if 'Convolution' is setting.FILTER[idx]:
                RESULT_IMG = convolution.processing(img)

            if 'Canny' is setting.FILTER[idx]:
                RESULT_IMG = canny.processing(img)

            if 'Erosion' is setting.FILTER[idx]:
                return img_list

            # 결과 저장
            self.filtering_img_list.append(RESULT_IMG)

        return self.filtering_img_list



