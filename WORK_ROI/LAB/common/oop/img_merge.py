"""
Created by SungMin Yoon on 2021-01-06..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import cv2 as cv


class Merge:

    # 기준이 되는 가장 큰 리스트
    mutable: list

    def __init__(self):
        self.mutable = list()

    def clear(self):
        self.mutable.clear()

    '''     Method explanation: set_list
        서로 다른 길이의 list 병합하기 위해
        1. 가장 큰 길이의 self.mutable 리스트가 기준이 되어
        2. 입력 리스트의 튜플 index 값을 보고 중간 중간 병합을 합니다.
        3. 다른 작은 리스트(input_list)를 계속 받아 들입니다..
    '''
    def mask_overwrite(self, size, input_list):

        # 입력된 작은 리스트
        count = len(input_list)

        # size 를 입력 받아 가장 큰 리스트를 만들고
        if len(self.mutable) == 0:
            self.mutable = [0]*size

        for i in range(0, count):

            # 인덱스 값을 가져오고
            mask, index = input_list[i]

            # 뮤테이블 의 해당 인덱스에 정보를 넣어 줍니다.
            if self.mutable[index] == 0:
                self.mutable[index] = (mask, index)
            else:
                # 뮤테이블의 마스크를 입력 마스크와 합하고 다시 뮤테이블에 저장합니다.
                mutable_mask, mutable_index = self.mutable[index]
                plus_mask = cv.add(mutable_mask, mask)
                self.mutable[mutable_index] = (plus_mask, mutable_index)

        # 병합 완료된 뮤테이블
        return self.mutable

    def roi_overwrite(self, size, input_list):

        count = len(input_list)

        if len(self.mutable) == 0:
            self.mutable = [0]*size

        for i in range(0, count):

            roi, index = input_list[i]

            if self.mutable[index] == 0:
                self.mutable[index] = (roi, index)
            else:
                mutable_roi, mutable_index = self.mutable[index]

                # # 필터를 만들어 바탕 이미지를 해치지 않고 결과 덮어 씌운다.
                # gray_filtered = cv.inRange(roi, 255, 255)
                #
                # plus_roi = cv.add(gray_filtered, mutable_roi)
                # self.mutable[mutable_index] = (plus_roi, mutable_index)

        return self.mutable




