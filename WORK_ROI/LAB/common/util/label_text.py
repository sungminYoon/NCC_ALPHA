"""
Created by SungMin Yoon on 2021-12-15..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""

import os
import time
from LAB.common.util import thumbnail
from LAB.common.util import notice
from PySide6.QtWidgets import QLabel


def setting_label(q_label: QLabel, q_value: QLabel, text):
    q_label.setText(text)
    q_label.setFixedHeight(30)
    q_value.setFixedHeight(30)


# 썸내일 이미지 만들기
def check_thumbnail(image_folder):
    print('call Menu: check_thumbnail')
    path = f'{image_folder}thumbnail'
    if not (os.path.isdir(path)):
        thumbnail.img_toThumbnail(image_folder, 'jpg')
        print('썸네일 이미지 만들기 완료!')
        time.sleep(0.1)
    else:
        print('썸네일 폴더가 이미 존재 합니다.')


# 입력값 초과시 메시지 알림
def check_value(str_value, limit_value, lowest_value):
    str1 = '는 사용 불가능한 값입니다.'
    str2 = '이상'
    str3 = '이하 값을 입력해 주세요'

    value = float(str_value)
    if limit_value < value or value < lowest_value:
        limit_message = f'{str_value} {str1} {lowest_value} {str2} {limit_value} {str3}'
        notice.message('Limit', limit_message)
        return True
    else:
        return False