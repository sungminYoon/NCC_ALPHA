"""
Created by SungMin Yoon on 2020-04-13..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
import time
from LAB.common.model.info import Info
from LAB.common.util import notice
from LAB.common.util import container
from LAB.common.util import img_level
from LAB.common.util import img_threshold


class Provider:
    dicom_set = None            # 다이콤 이미지 모음 세트
    info_list = None            # 이미지 정보 데이터 리스트를 만듭니다.
    img_container = None        # Open cv 이미지 모음 입니다.
    img_level_list = None       # 이미지 LEVEL 변환 모음 입니다.
    img_group_level = None      # 이미지 업데이트에 사용되는 리스트 입니다.
    img_group_threshold = None  # 이미지 광역 쓰레숄드 리스트

    def __init__(self):
        self.info_list = []
        self.img_container = []
        self.img_group_level = []
        self.img_group_threshold = []

    # dicom -> cv image
    def create_dicom(self, dicom_folder):
        self.dicom_set = container.set_DicomToCv(dicom_folder)

    # jpg,png image -> cv image
    def create(self, data_folder, extension):

        file_list = os.listdir(data_folder)
        file_list.sort()
        file_list_img = [file for file in file_list if file.endswith(extension)]

        # container 에서 image_set 을 생성합니다.
        self.img_container = container.set_cv_image(data_folder, file_list_img)

        # container 에서 image_set 파일쓰기 시간을 줍니다.
        time.sleep(1)
        print('Provider: Open cv image data set 생성을 완료 했습니다.')

        # 모델 객체에 입력 해주고
        i = 0
        for name in file_list_img:
            info = Info()
            info.image_name = name
            info.image_path = f'{data_folder}{name}'
            info.image_thumbnail = f'{data_folder}thumbnail/thumbnail_{name}'
            info.image_annotation = None
            info.image_data = self.img_container[i]

            self.info_list.append(info)
            i = i + 1

    def get_data_path(self, index):
        info = self.info_list[index]
        return info.image_path

    def data_read(self):
        for info in self.info_list:
            print('image_name', info.image_name)
            print('image_path', info.image_path)
            print('image_thumbnail', info.image_thumbnail)
            print('image_annotation', info.image_annotation)
            print('image_roi', info.image_roi)
            print('image_data', True if info.image_data is not None else False)
            print('----------------------------------------------')

    # 넘버와 이미지 가 들어간 GRAY 스케일 CV 이미지 업데이트
    def data_update_level(self, window, muscle):

        if self.img_container is None:
            print('Provider: data_update_level ERROR')
            return

        notice.message('변환', '이미지 업데이트 합니다.')
        self.img_group_level.clear()

        # RGB 스케일 레벨을 합니다.
        temp_list = []
        for img in self.img_container:
            level_image = img_level.tissue_process(img,
                                                   0,
                                                   window,
                                                   muscle,
                                                   0.1)

            temp_list.append(level_image)

        # 넘버를 넣어 줍니다.
        i: int = 1
        for img in temp_list:
            group = (img, i)
            i = i + 1
            self.img_group_level.append(group)

        self.img_level_list = None
        self.img_level_list = temp_list
        notice.message('변환', '변환 완료했습니다.')

        return self.img_group_level

    def data_update_threshold(self):

        self.img_group_threshold.clear()

        # RGB 스케일 레벨을 합니다.
        temp_list = []
        for cv_image in self.img_level_list:
            gray_img = img_threshold.all_bgr(cv_image)
            temp_list.append(gray_img)

        # 넘버를 넣어 줍니다.
        i: int = 1
        for img in temp_list:
            group = (img, i)
            i = i + 1
            self.img_group_threshold.append(group)

        return self.img_group_threshold

    def data_del(self):
        pass
