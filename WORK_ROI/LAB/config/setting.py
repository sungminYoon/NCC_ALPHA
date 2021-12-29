"""
Created by SungMin Yoon on 2021-03-09..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""

'''WINDOW'''
TITLE_WINDOW = 'NCC AUTO ROI'   # 응용프로그램 이름
WINDOW_SCREEN_WIDTH = 950   # 응용프로그램 창 가로크기
WINDOW_SCREEN_HEIGHT = 800  # 응용프로그램 창 세로 크기

'''COMMON'''
USER_CHOICE_COUNT = 9   # 사용자 UI TOOL Threshold 선택 가능한 개수

''' FILTER '''
FILTER = ('Normal', 'Gaussian', 'Laplace', 'Convolution', 'Canny', 'Erosion')

'''TOOL'''
DEFAULT_LEVEL_WINDOW = 800  # 초기값
DEFAULT_LEVEL_MUSCLE = 0    # 초기값

'''AUTO'''
PARAM_LEVEL_MUSCLE = 650    # 근육 초기값
MINIMUM_DISTANCE = 10       # 인접한 roi 영역과 사용자 roi 사이 최소 거리 입니다.
LEVEL_MARGIN = 50           # 선택한 level 값에 (플러스, 마이너스 50 + 50 = 100 회) 루틴 값입니다.

'''Menu'''
THRESHOLD = 20          # 초기값
PROPERTY_MAX = 300      # roi 찾기 최대 크기
PROPERTY_MIN = 10       # roi 찾기 최소 크기

'''COLOR'''
ROI_COLOR = [(13, 214, 242),
             (0, 128, 0),
             (0, 0, 250),
             (250, 128, 250),
             (128, 128, 250),
             (0, 250, 200),
             (0, 250, 0),
             (255, 0, 0),
             (30, 128, 128)]



