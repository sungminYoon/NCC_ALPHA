"""
Created by SungMin Yoon on 2021-05-18..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PySide6 import QtCore, QtWidgets
from LAB.common.util import img_threshold
from LAB.common.util import img_convert_qt


class ViewSecond(QtWidgets.QGraphicsView):

    screen_rect: QtCore.QRectF = None

    # QT 예제 기본 VIEW 구조
    def __init__(self, parent=None):
        super(ViewSecond, self).__init__(parent)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.q_graphic = QtWidgets.QGraphicsPixmapItem()
        self.scene.addItem(self.q_graphic)
        self.setScene(self.scene)

    def setup(self):
        self.screen_rect: QtCore.QRectF = QtCore.QRectF(0.0, 0.0, 513, 513)
        self.setSceneRect(QtCore.QRectF(self.screen_rect))

    def update_screen(self, cv_image):
        print('ViewSecond: update_screen')
        color_img = img_threshold.all_bgr(cv_image)
        pix_image = img_convert_qt.bgr_to_pixImage(color_img)

        self.q_graphic.setPixmap(pix_image)
        self.repaint()
