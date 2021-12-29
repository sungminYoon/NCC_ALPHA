"""
Created by SungMin Yoon on 2021-05-24..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import time
import cv2 as cv
from LAB.common.util import img_empty

DEFECTS = None


# 마스크 컨투어 처리 함수 입니다.
def contour_to_bgr(img_gray):
    print('img_threshold: contour_to_bgr')
    global DEFECTS

    # 일반적인 threshold 로직
    cv_image = cv.cvtColor(img_gray, cv.COLOR_BGR2RGB)
    ret, th = cv.threshold(img_gray, 127, 255, 0)
    contours, hierarchy = cv.findContours(th, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # 컨투어 로직
    loop_count: int = 0
    contours_list = []
    for cnt in contours:
        loop_count = loop_count + 1
        dot_list = []

        # 빈 이미지
        h, w = img_gray.shape[:2]
        mask = img_empty.cv_image(h, w)

        # 빈 이미지에 마스크 그리기
        cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)

        # 마스크 그리기 지연처리
        time.sleep(0.1)

        # 마스크 사이즈
        chk_size = cv.countNonZero(mask)

        # 컨투어를 그릴 수 있는 마스크 크기면 실행
        if chk_size > 100:

            # 볼록 선체 찾기(인덱스 기준)
            hull2 = cv.convexHull(cnt, returnPoints=False)

            ''' Error 예외 처리 '''
            try:
                # 볼록 선체 결함 찾기
                DEFECTS = cv.convexityDefects(cnt, hull2)
            except cv.error:
                DEFECTS = None

            try:
                DEFECTS.shape[0]
            except AttributeError:
                DEFECTS = None

            if DEFECTS is None:
                dot_list.append(0)
                pass
            else:
                # 볼록 선체 결함 순회
                for i in range(DEFECTS.shape[0]):

                    # 시작, 종료, 가장 먼 지점, 거리
                    startP, endP, farthestP, distance = DEFECTS[i, 0]

                    # 가장 먼 지점의 좌표 구하기
                    farthest = tuple(cnt[farthestP][0])

                    # 거리를 부동 소수점으로 변환
                    dist = distance / 256.0

                    # 거리가 0.1보다 큰 경우
                    if dist > 0.1:
                        dot_list.append(farthest)

                        # 빨강색 점 표시
                        cv.circle(cv_image, farthest, 1, (0, 0, 255), -1)

        t = (loop_count, dot_list)
        contours_list.append(t)

    return cv_image, contours_list


# GRAY 처리 광역쓰레숄드 입니다.
def all_bgr(cv_image):
    print('img_threshold: all_bgr')

    img_gray = cv.cvtColor(cv_image, cv.COLOR_BGR2GRAY)
    ret, img_binary = cv.threshold(img_gray, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # (255, 0, 0) 파란색
        cv.drawContours(cv_image, [cnt], 0, (255, 0, 0), 1)

    return cv_image


# BGR2RGB 처리 광역 쓰레숄드 입니다.
def all_gray_to_bgr(img_gray):
    print('img_threshold: all_gray_to_bgr')

    cv_image = cv.cvtColor(img_gray, cv.COLOR_BGR2RGB)
    ret, img_binary = cv.threshold(img_gray, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # (255, 0, 0) 파란색
        cv.drawContours(cv_image, [cnt], 0, (255, 0, 0), 1)

    return cv_image


# 사각형으로 그려 줍니다.
def all_rectangle(cv_image):
    print('img_threshold: all_rectangle')

    ret, img_binary = cv.threshold(cv_image, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # 관심 영역 사각형 표시
        x, y, w, h = cv.boundingRect(cnt)
        cv_image = cv.rectangle(cv_image, (x, y), (x + w, y + h), (255, 255, 255), 1)

    return cv_image


# 빈이미지에 쓰레숄드를 전부 그립니다.
def all_mask(image):
    print('img_threshold: all_mask')

    cut_img_list: list = []

    ret, img_binary = cv.threshold(image, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        h, w = image.shape[:2]
        mask = img_empty.cv_image(h, w)
        cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)
        cut_img_list.append(mask)

    return cut_img_list


# 쓰레숄드의 좌표를 리스트 형태로 반환 합니다.
def all_cnt(image):
    print('img_threshold: all_cnt')

    cnt_list: list = []

    ret, img_binary = cv.threshold(image, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        cnt_list.append(cnt)

    return cnt_list


# 쓰레숄드의 크기가 적정 50 크기인지 확인 합니다.
def all_mask_chk(image):
    print('img_threshold: all_mask_chk')

    ret, img_binary = cv.threshold(image, 127, 255, 0)
    contours, hierarchy = cv.findContours(img_binary, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        # 빈 이미지
        h, w = image.shape[:2]
        mask = img_empty.cv_image(h, w)

        # 빈 이미지에 마스크 그리기
        cv.drawContours(mask, [cnt], 0, (255, 0, 0), cv.FILLED)

        # 마스크 그리기 지연처리
        time.sleep(0.1)

        # 마스크 사이즈
        chk_size = cv.countNonZero(mask)

        # 컨투어를 그릴 수 있는 마스크 크기면 실행
        if chk_size > 50:
            chk = True
        else:
            chk = False

    return chk
