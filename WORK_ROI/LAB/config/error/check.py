"""
Created by SungMin Yoon on 2020-06-29..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
import fnmatch


# json 확장자 확인
def extension_json(_folder):
    for file in os.listdir(_folder):
        if fnmatch.fnmatch(file, '*.json'):
            return True
        else:
            print('error: ')
            return False


# DICOM 확장자 확인
def extension_dicom(_folder):
    for file in os.listdir(_folder):
        if fnmatch.fnmatch(file, '*.dcm'):
            return True
        else:
            print('error: ')
            return False


# PNG 확장자 확인
def extension_png(_folder):
    print('error: extension_png')

    for file in os.listdir(_folder):
        if fnmatch.fnmatch(file, '*.png'):
            return True
        else:
            return False


# jpg 확장자 확인
def extension_jpg(_folder):
    print('error: extension_jpg')

    for file in os.listdir(_folder):
        if fnmatch.fnmatch(file, '*.jpg'):
            return True
        else:
            return False


# List type error 체크
def error_type_chk(param_list):
    print(param_list)
    pass
