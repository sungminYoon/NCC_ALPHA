"""
Created by SungMin Yoon on 2020-05-06..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import time
import numpy as np
from LAB.common.model.roi import Roi
from PIL import Image  # setting 에서 Pillow 설치


def to_binary_loop(day_folder, src_list):
    # src_list 형식은 개발자 임의 형태 입니다. -> list[int_obj(tuple (value, value))]
    for i in range(0, len(src_list)):
        int_obj = src_list[i]

        # 리스트에서 obj 를 가지고 옵니다.
        if src_list[i] == 0:
            pass
        else:
            src, index = int_obj

            # img 파일을 numpy 로 변환 합니다.
            img = np.array(src)

            # 이미지의 128 값 보다 색이 높은 곳을 1이라는 값으로 numpy -> binary 변환 합니다.
            binary = np.where(img > 128, 1, 0)

            # binary 를 reshape( , )2차원 (1, )1줄 ( , -1) 나머지 자동 맞춤 후 TEXT 저장합니다.
            file_name = f'{index}'
            path = f'{day_folder}/{file_name}.text'
            np.savetxt(path, binary.reshape(1, -1), fmt="%s", header='')

            # 파일 저장할 시간을 주고
            time.sleep(0.5)


def to_binary(folder, src, file_name, classification):
    # png 파일을 numpy 로 변환 합니다.
    img = np.array(src)

    # 이미지의 128 값 보다 색이 높은 곳을 1이라는 값으로 numpy -> binary 변환 합니다.
    binary = np.where(img > 128, 1, 0)

    # binary 를 reshape( , )2차원 (1, )1줄 ( , -1) 나머지 자동 맞춤 후 TEXT 저장합니다.
    file_name = f'{classification}_{file_name}'
    path = f'{folder}/{file_name}'

    np.savetxt(path, binary.reshape(1, -1), fmt="%s", header='')

    # 파일 저장할 시간을 주고
    time.sleep(0.5)


def to_image(file_name):
    # TEXT -> IMAGE
    with open(file_name, mode='r') as file:
        fileContent = file.read().split(' ')
        value = []

        # STRING binary 를 INT binary 변환 합니다.
        i = 1
        count = len(fileContent)
        for obj in fileContent:
            if i == count:
                break

            # (512 * 512 = 262144)
            if i > 262144:
                break

            try:
                num = int(obj)
                value.append(num)

            # 마지막 줄 바꿈 STRING 은 예외 처리 합니다.
            except ValueError:
                value.append(0)
                break
            i = i + 1

        # INT binary 를 이미지로 변경 합니다.
        img = Image.new('1', (512, 512), "black")
        img.putdata(value)

        # 파일 이름만 가져오기
        if file_name.count(".") == 1:  # . 이 한개일떄
            V = file_name.split(".")
            print("file Name : " + V[0])

        # 파일을 저장합니다.
        file_make = f'{V[0]}.jpg'
        img.save(file_make)


def list_compare(export_list, user_select_list):
    for i in range(0, len(export_list)):
        obj = export_list[i]

        if obj is 0:
            pass
        else:
            _, _number = obj
            a: int = int(_number)
            user_select = user_select_list
            for _object in user_select:
                number, chk = _object
                b: int = int(number)
                if a == b:
                    if chk is False:
                        export_list[i] = 0
                        print('mask_export:', i)

    return export_list


def to_1_dimension(export_list):
    print('img_text: to_1_dimension')

    # 1차원 리스트 생성
    one_dimension_list = []

    # 내보내기 리스트 roi 리스트 분리
    for i in range(0, len(export_list)):
        roi_list = export_list[i]

        # roi 리스트 에서 roi 분리
        for j in range(0, len(roi_list)):

            # 리스트 에서 튜플 꺼내기
            tuple_obj = roi_list[j]

            # 튜플에서 roi 꺼내기
            obj: Roi = tuple_obj[1]

            # 인덱스 번호 만들기
            str_number = f'{i+1}_{tuple_obj[0]}'
            tuple_roi = (obj.image_mask, str_number)

            # 1차원 리스트 저장
            one_dimension_list.append(tuple_roi)

    # 1차원 리스트 반환
    return one_dimension_list
