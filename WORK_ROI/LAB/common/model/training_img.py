"""
Created by SungMin Yoon on 2021-11-25..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import os
import time
import imageio
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from LAB.common.util import img_text
from PIL import Image


# 정답 데이터를 만듭니다.
def dataset_y(path):

    y = []      # 정답 데이터 저장 공간
    name = []   # 정답 데이터 이름 저장 공간

    # 경로, 폴더, 파일 리스트
    for r, d, f in os.walk(path):

        # 파일 text -> image 로 변환
        for file_name in f:
            if '.text' in file_name:
                text_path = os.path.join(r, file_name)
                img_text.to_image(text_path)

        # 이미지 파일을 저장할 시간을 줍니다.
        time.sleep(1)

        for img_name in f:
            if '.jpg' in img_name:

                # jpg 파일 경로를 가져 옵니다.
                image_path = os.path.join(r, img_name)

                # 이미지를 데이터로 읽어 드립니다.
                with open(image_path, 'rb') as file_image:
                    data = file_image.read()

                # 데이터를 numpy unit8 로 인코딩 합니다.
                encoded_img = np.fromstring(data, dtype=np.uint8)

                # 3차원 IMREAD_COLOR 인코딩 합니다.
                img = cv.imdecode(encoded_img, cv.IMREAD_GRAYSCALE)
                y.append(img)

                # 파일 이름만 따로 저장 합니다.
                name.append(img_name)

    return y, name


# 폴더의 jpg 파일 리스트를 가지고 옵니다.
def file_jpg_list(_folder_path):
    file_list = os.listdir(_folder_path)
    jpg_list = [file for file in file_list if file.endswith(".jpg")]
    return jpg_list


# 훈련 데이터를 만듭니다.
def dataset_x(path, choice_list):
    print('training_img: dataset_x')

    # 훈련용 데이터 저장 공간 생성
    x = []

    # 정답 데이터
    choice_set = set(choice_list)

    # 훈련용 데이터가 있는 리스트
    file_list = file_jpg_list(path)

    for full_name in file_list:
        for num in choice_set:

            # 훈련용 데이터와 정답 데이터가 일치하면 저장
            if num in full_name:
                print('training: ', num, ':', full_name)
                image_path = f'{path}{full_name}'

                # 이미지를 데이터로 읽어 드립니다.
                with open(image_path, 'rb') as file_image:
                    data = file_image.read()

                # 데이터를 numpy unit8 로 인코딩 합니다.
                encoded_img = np.fromstring(data, dtype=np.uint8)

                '''image 복원 코드 세이브'''
                # 3차원 IMREAD_COLOR 인코딩 합니다.
                img = cv.imdecode(encoded_img, cv.IMREAD_GRAYSCALE)

                # img_array = np.array(img)
                # pil_image = Image.fromarray(img_array)
                # pil_image.show()

                x.append(img)
    return x



