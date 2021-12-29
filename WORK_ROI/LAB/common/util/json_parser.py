"""
Created by SungMin Yoon on 2021-11-04..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""

import json

from datetime import datetime
from LAB.config.path import file_manager


def depth_one(info_list):

    # 좌표 딕셔너리를 만들고
    position_dict = dict()

    # 좌표 정보를 꺼내서
    for info in info_list:

        # 좌표 딕셔너리에 key = 좌표 그룹 번호, value = 좌표 리스트 넣어 줍니다.
        position_dict[info[0]] = depth_two(info[1])

    # 좌표 딕셔너리 반환
    return position_dict


def depth_two(position_list):

    # 포지션 그룹 리스트를 만듭니다.
    position_group = []

    # 포지션 리스트에서
    for obj in position_list:

        try:
            # 좌표를 가져오고
            x = f'{obj[0]}'
            y = f'{obj[1]}'

        except TypeError:
            x = '0'
            y = '0'

        # 인덱스 키에 값을 넣어 주고
        position = dict()
        position['x'] = x
        position['y'] = y

        # 좌표 딕셔너리를 저장 합니다.
        position_group.append(position)

    # 좌표 리스트 반환
    return position_group


# 마스크 위치 좌표를 JSON 파일로 저장 합니다.
def mask_position_save_text(path, data_list):
    print('json_parser: mask_position_save_text')

    # 컨투어 그룹 리스트를 만듭니다.
    contour_group = []

    for image_info in data_list:

        # 딕셔너리를 생성 합니다.
        image_number = dict()
        image_number['number'] = image_info[0]
        image_number['contours'] = depth_one(image_info[1])

        # 이미지 넘버를 컨투어즈 그룹에 저장
        contour_group.append(image_number)

    # 결과를 파일로 저장 합니다.
    json_file_save(path, contour_group)


# json 파일로 저장 합니다.
def json_file_save(path, json_data):
    # 파일 이름을 날짜, 시간 으로 만듭니다.
    folder_path = file_manager.folder_name(path)
    file_name = datetime.today().strftime("%Y%m%d%H%M%S")
    file_extension = f'.json'
    file_path = f'{folder_path}{file_name}{file_extension}'

    # 파일 경로, 이름을 가지고 json 형식으로 저장 합니다.
    with open(file_path, 'w', encoding='utf-8') as make_file:
        json.dump(json_data, make_file, indent="\t")
