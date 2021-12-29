"""
Created by SungMin Yoon on 2021-05-24..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PySide6 import QtGui


# cv 이미지를 Gray_scale8 Q_Pix_map 변환 합니다.
def gray_to_pixImage(gray_img):
    height, width = gray_img.shape[:2]
    g_image = QtGui.QImage(gray_img, width, height, QtGui.QImage.Format_Grayscale8)
    pix_image = QtGui.QPixmap.fromImage(g_image)
    return pix_image


# cv 이미지를 BGR888 Q_Pix_map 변환 합니다.
def bgr_to_pixImage(bgr_img):
    height, width = bgr_img.shape[:2]
    _image = QtGui.QImage(bgr_img, width, height, QtGui.QImage.Format_BGR888)
    pix_image = QtGui.QPixmap.fromImage(_image)
    return pix_image
