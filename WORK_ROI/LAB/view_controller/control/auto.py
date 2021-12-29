"""
Created by SungMin Yoon on 2021-06-15..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import numpy as np
import cv2 as cv
from LAB.config import setting
from LAB.common.util import img_threshold, point2D, img_level, img_empty
from LAB.common.model.roi import Roi
from LAB.common.oop.img_merge import Merge


class Auto:
    """
        단어 설명
        threshold -> 사용자가 선택한 영역입니다.
        mask -> 선택 또는 찾은 영역의 이미지 입니다.
        roi -> 사용자가 선택한 threshold 와 mask 정보를 model 객체로 변환한 "관심영역" 입니다.
    """

    level_window = setting.DEFAULT_LEVEL_WINDOW  # 윈도우 레벨
    level_muscle = setting.PARAM_LEVEL_MUSCLE  # 근육 레벨

    call_progress = None  # 콜백 객체로 진행상황을 알립니다.
    img_all_count = None  # 입력 받은 CV IMAGE 들 전체 개수

    merge: Merge    # 이미지 병합 객체
    user_roi: Roi   # roi 모델 객체
    standard_roi: Roi   # roi 모델 객체

    min_value: int = 0  # mask 최소 크기
    max_value: int = 0  # mask 최대 크기

    color_list: list    # 무수정 image 에 mask 색칠한 이미지 입니다.
    roi_list: list      # roi 모델 객체 리스트
    group_list: list    # user_roi 처리 list 모음  : n 저장

    def __init__(self):
        print('Auto: init')
        self.roi_list = []
        self.group_list = []
        self.color_list = []

        # 병합 객체 생성
        self.merge = Merge()

    def clean(self):
        self.roi_list.clear()
        self.group_list.clear()
        self.color_list.clear()

    # 사용자 선택 mask 를 roi 로 변환 합니다.
    def create_roi(self, mask_list):
        print('Auto: create_roi')

        # 사용자 선택 roi mask 만큼 반복
        length = len(mask_list)
        for i in range(0, length):

            # 사용자 선택 mask 가져오기
            img = mask_list[i]

            if img is None:
                print('Auto: create_roi -> img is None')
            else:
                # mask 이미지를 roi 모델 객체로 저장
                roi = Roi()
                roi.set_mask(img)
                self.roi_list.append(roi)

    # 이미지 roi 처리를 시작합니다.
    def process_roi(self, cv_images, start_point, end_point, user_select_index):
        print('Auto: process_roi')

        call = self.call_progress
        call(100, 0)

        # 정수형으로 변환
        if start_point is None:
            start_point = 1
        start = int(start_point)
        end = int(end_point)

        # 사용자 지정 인덱스
        middle = user_select_index

        # 사용자 지정 윈도우, 근육 값
        window = int(self.level_window)
        muscle = int(self.level_muscle)

        # 전체 이미지 개수
        self.img_all_count = len(cv_images)

        # 사용자 선택 roi 개수 만큼 반복
        length = len(self.roi_list)
        for user_mask_count in range(0, length):

            # 사용자 선택 roi
            self.user_roi = self.roi_list[user_mask_count]

            # 1주기 결과를 저장하는 리스트 생성
            one_cycle_list = []

            # 기준이 되는 roi 를 저장하고
            self.standard_roi = self.user_roi

            # 아래로 찾기
            i = 0
            for _ in range(start, middle):
                index = middle - i
                img = cv_images[index]

                # 사용자 종료 지점이 카운트 보다 크면
                if index > start:

                    # images level 나누기
                    level_list = self._level_break(img, window, muscle)

                    # level_images 비교 처리
                    process_list = self._level_compare(self.user_roi, level_list)

                    # process_list 에서 넓이가 user_roi 가장 비슷한것 찾기
                    tuple_roi = self._find_roi(self.user_roi, process_list, index)

                    # 결과를 list 저장
                    one_cycle_list.append(tuple_roi)
                else:
                    print('up find 완료')
                i = i + 1

                # 진행바
                call = self.call_progress
                call(end, i)

            '''------------------------------------------------------------------------------------------------------'''
            # 기준을 원래 대로 해주고
            self.user_roi = self.standard_roi

            # 위 로 찾기
            j = 1
            for _ in range(middle, end):
                index = middle + j

                # 인덱스 에러 방지
                if index >= len(cv_images):
                    return

                img = cv_images[index]

                # 사용자 종료 지점이 카운트 보다 크면
                if index < end:

                    # images level 나누기
                    level_list = self._level_break(img, window, muscle)

                    # level_images 비교 처리
                    process_list = self._level_compare(self.user_roi, level_list)

                    # process_list 에서 넓이가 user_roi 가장 비슷한것 찾기
                    tuple_roi = self._find_roi(self.user_roi, process_list, index)

                    # 결과를 list 저장
                    one_cycle_list.append(tuple_roi)
                else:
                    print('end find 완료')

                # 진행바
                j = j + 1
                call = self.call_progress
                call(end, j)

            # 1주기 user_roi 를 무수정 이미지에 색칠 합니다.
            self._change_mask_color(one_cycle_list, cv_images, user_mask_count)

            # 1주기 user_roi 저장 그룹화
            self.group_list.append(one_cycle_list)

        # 이미지 포멧을 변경합니다.
        for img in self.color_list:
            cv.cvtColor(img, cv.COLOR_RGB2BGR)

        # 리스트 그룹을 하나의 결과 리스트로 만듭니다.
        result = self._result_image(self.group_list)

        # 처리 결과 내보내기
        return result, self.group_list

    # 1주기 user_roi 를 무수정 이미지에 색칠 합니다.
    def _change_mask_color(self, cycle_list, cv_images, user_mask_count):

        # 색을 만들어 저장 합니다.
        roi_color: list = []

        for i in range(0, setting.USER_CHOICE_COUNT):

            a, b, c = setting.ROI_COLOR[i]
            roi_color.append(tuple([a, b, c]))

        if 1 > len(self.color_list):
            # 무수정 이미지를 복사합니다.
            self.color_list = cv_images.copy()

        # roi 처리된 리스트에서 정보를 가져 옵니다.
        for obj in cycle_list:

            if obj is None:
                pass
            else:
                index, roi = obj

                # 무수정 이미지를 가져옵니다.
                img = self.color_list[index]

                # 첫번째 이미지 만 포맷 변환 합니다.
                if user_mask_count == 0:
                    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

                # mask 의 threshold 가져옵니다.
                _, binary = cv.threshold(roi.image_mask, 127, 255, 0)
                contours, _ = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

                for cnt in contours:

                    # roi 를 그려주고 색칠합니다.
                    a, b, c = roi_color[user_mask_count]
                    cv.drawContours(img, [cnt], 0, (a, b, c), cv.FILLED)

                # 색칠한 이미지를 리스트에 저장 합니다.
                self.color_list[index] = img

    # 사용자 roi 와 가장 비슷한 roi 를 찾습니다.
    def _find_roi(self, change_roi, process_list, image_index):
        print('Auto: _find_roi')

        # standard_roi 와 가장 비슷한 넓이의 roi
        dimension_list = []

        # 데이터가 없으면 종료
        if len(process_list) < 1:
            return

        # 리스트 속의 roi 객체의 넓이를 따로 저장합니다.
        for obj in process_list:
            roi: Roi = obj
            dimension_list.append(roi.rect_dimensions)

        # 사용자 roi 넓이와 가장 가까운 값의 number 찾습니다.
        number = self.min_diff_pos(dimension_list, change_roi.rect_dimensions)
        find_roi = process_list[number]

        # 찾은 roi 로 기준을 바꿔 줍니다.
        self.user_roi = find_roi

        # 이미지 인덱스와 roi 묶어 보내기
        print('Auto: _find_roi -> image_index = ', image_index)
        _tuple = (image_index, find_roi)
        return _tuple

    # 그룹 을 하나의 결과로 만듭니다.
    def _result_image(self, group):
        print('Auto: _result_image')

        # 결과 저장 리스트
        result_list = None

        # 그룹에서 처리 완료된 roi 리스트 가져오기
        for i in range(0, len(group)):

            # 병합(self.merge.mask_overwrite) 파라미터 에 넣기 위한 형식으로 변환
            mask_list = []
            for _obj in group[i]:

                # obj 에 객체 예외 처리
                roi: Roi
                try:
                    # 리스트 객체의 하위 객체를 가져옵니다.
                    roi = _obj[1]
                    image_index = _obj[0]

                    # mask 리스트 저장
                    mask = (roi.image_mask, image_index)
                    mask_list.append(mask)

                # obj 객체 error 처리
                except TypeError as e:
                    print('Auto: _result_image -> ', e)
                    pass

            # 완료 mask 병합
            result_list = self.merge.mask_overwrite(self.img_all_count, mask_list)

        # 결과 리스트
        return result_list

    # 이미지를 level 로 나눕니다.
    @classmethod
    def _level_break(cls, img, level_window, level_muscle):

        # 리스트 초기화
        level_list = []

        # level_start ~ level_end 까지 반복
        level_start = level_muscle - setting.LEVEL_MARGIN
        level_end = level_muscle + setting.LEVEL_MARGIN

        for level in range(level_start, level_end):

            # 이미지 레벨링
            level_image = img_level.tissue_process(img, 0, level_window, level, 0.1)

            # level 결과 저장
            level_list.append(level_image)

        # level 처리완료 리스트
        return level_list

    # level 로 나눈 이미지를 비교 합니다.
    @classmethod
    def _level_compare(cls, standard_roi, level_images):
        print('Auto: _level_compare')

        # 리스트 초기화
        process_list = []

        # level 이미지 roi 처리 시작
        for img in level_images:

            # 처리 이미지의 크기를 저장하고
            h, w = img.shape[:2]

            # 이미지 하나에 대한 모든 쓰레숄드 좌표 리스트
            threshold_list = img_threshold.all_cnt(img)

            for cnt in threshold_list:

                # 모멘트 알고리즘 사용
                M = cv.moments(cnt)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                else:
                    # 쓰레숄드 중심 좌표를 가져옴
                    cX, cY = 0, 0

                # 2점 사이 거리
                dist = point2D.dot_distance(standard_roi.rect_center_x,
                                            standard_roi.rect_center_y,
                                            cX,
                                            cY)

                # MINIMUM_DISTANCE 미만의 거리 만 roi 변경 저장
                if dist < setting.MINIMUM_DISTANCE:
                    print('Auto: _level_compare -> mask generating..')
                    mask = img_empty.cv_image(h, w)
                    cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)

                    # roi 생성
                    roi = Roi()
                    roi.set_mask(mask)

                    # roi 저장
                    process_list.append(roi)

        # 처리 완료 리스트
        return process_list

    # 가장 비슷한 값을 찾는 로직
    @classmethod
    def min_diff_pos(cls, array_like, target):
        return np.abs(np.array(array_like) - target).argmin()
