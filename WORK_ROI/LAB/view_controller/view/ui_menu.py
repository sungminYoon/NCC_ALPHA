"""
Created by SungMin Yoon on 2020-04-27..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import os
import time

from PySide6 import QtGui
from PySide6.QtWidgets import *
from LAB.common.util import img_convert_dicom
from LAB.common.util import notice
from LAB.common.util import label_text
from LAB.config import path
from LAB.config.path import file_manager
from LAB.config.error import messages, check


TITLE_IMG_DICOM = '1. Dicom -> Image 512x512'
TITLE_IMG_LOAD = '2. Load image'
TITLE_ALGORITHM = '3. Pre-processing'
TITLE_EXPORT = '4. Export ROI'
TITLE_SELECTION_IMAGE = 'No select image'


class Menu(QVBoxLayout):

    call_scroll = None              # call_back 객체 입니다. 스크롤 데이터를 생성 또는 가지고 옵니다.
    call_export = None              # call_back 객체 입니다. mask 이미지를 2진 바이너리 데이터로 내보냅니다.
    call_algorithm = None           # call_back 객체 입니다. 알고리즘 처리를 합니다.

    file_extension = None           # 선택된 파일 확장자 입니다.
    label_current_image = None      # 선택된 이미지 입니다.

    menu_group = None               # 메뉴 그룹 입니다.

    label_logo = None               # 상단 라벨 이미지.
    dicom_btn = None                # dicom 폴더의 모든 dicom 에서 이미지를 꺼내 png 로 변환 합니다.
    load_btn = None                 # png 폴더의 모든 이미지를 스크롤에 불러 옵니다.
    export_btn = None               # 이진 바이너리 데이터로 내보냄
    algorithm_btn = None            # 알고리즘 처리 버튼 입니다.

    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)
        print('Menu: init')

        self.file_extension = 'jpg'

        # logo label
        logo_image = QtGui.QPixmap.fromImage(path.UI_MENU_LOGO)

        # 이미지 크기를 조종, 줄입니다.
        logo_image.setDevicePixelRatio(2.7)
        self.label_logo = QLabel()
        self.label_logo.setScaledContents(True)
        self.label_logo.setPixmap(logo_image)

        # DICOM 파일에서 이미지 파일 꺼내기
        self.dicom_btn = QPushButton(TITLE_IMG_DICOM)
        self.dicom_btn.clicked.connect(self.changDicomButtonClicked)
        self.dicom_btn.setStyleSheet("QPushButton { text-align: left; }")

        # 이미지 불러오기 버튼
        self.load_btn = QPushButton(TITLE_IMG_LOAD)
        self.load_btn.clicked.connect(self.loadButtonClicked)
        self.load_btn.setStyleSheet("QPushButton { text-align: left; }")

        # 내보내기 버튼
        self.export_btn = QPushButton(TITLE_EXPORT)
        self.export_btn.clicked.connect(self.exportButtonClicked)
        self.export_btn.setStyleSheet("QPushButton { text-align: left; }")

        # 알고리즘 처리 버튼
        self.algorithm_btn = QPushButton(TITLE_ALGORITHM)
        self.algorithm_btn.clicked.connect(self.algorithmButtonClicked)
        self.algorithm_btn.setStyleSheet("QPushButton { text-align: left; }")

        # 선택 된 이미지 (넘버)표시 라벨
        self.label_current_image = QLabel()
        self.label_current_image.setText(TITLE_SELECTION_IMAGE)
        self.label_current_image.setFixedHeight(30)

        # background-color
        self.label_current_image.setStyleSheet("background-color: lightYellow")

        # ui 화면에 올리기
        self.ui_setup()

    def ui_setup(self):

        # 위젯: 그룹
        self.menu_group = QVBoxLayout()
        self.menu_group.addWidget(self.label_logo)
        self.menu_group.addWidget(self.dicom_btn)
        self.menu_group.addWidget(self.load_btn)
        self.menu_group.addWidget(self.algorithm_btn)
        self.menu_group.addWidget(self.export_btn)

        # 현제 사용자가 선택한 이미지 넘버를 보여 줍니다.
        self.menu_group.addWidget(self.label_current_image)

        # 메뉴 그룹을 베이스 레이아웃에 등록 합니다.
        self.addLayout(self.menu_group)

    def exportButtonGreenColor(self):
        print('menu: exportButtonGreenColor')
        self.export_btn.setStyleSheet('background-color: lightGreen')

    def exportButtonGrayColor(self):
        print('menu: exportButtonGrayColor')
        self.export_btn.setStyleSheet('background-color: lightGray')

    def changeLabel(self, text):
        print('call Menu: changeLabel')
        self.label_current_image.setText(text)

    # mark - Event method
    def changeLevelButtonClicked(self):
        print('call Menu: changeLevelButtonClicked')
        call = self.call_change_level
        call()

    # mark - Event method
    def changDicomButtonClicked(self):
        print('call Menu: changButtonClicked')

        # 사용자가 선택한 파일경로
        file_path = file_manager.file_open()

        if file_path is 0:
            return

        # 사용자가 선택한 파일이름
        last_name = file_path[file_path.rfind('/') + 1:]

        # 파일이름의 경로 폴더명
        dicom_folder = file_path.replace(last_name, '', 1)

        notice.message('messages..', '아래 Yes 를 누르면 파일 변환을 시작합니다. 잠시만 기다려 주세요...')

        if check.extension_dicom(dicom_folder):
            # 폴더에 들어 있는 DICOM 에서 PNG 파일 내보내기
            img_folder = file_manager.make_folder(dicom_folder)
            img_convert_dicom.dicom_imageToImg(dicom_folder, img_folder, self.file_extension)
            print('DICOM 파일에서', {self.file_extension}, '파일 내보내기 완료!')

            # 0.1초 delay 후
            time.sleep(0.1)

            # 썸내일 이미지 만들기
            label_text.check_thumbnail(img_folder)

            # Window 메소드를 호출하여 scroll 에 경로 데이터를 보냅니다.
            call_data = self.call_scroll
            call_data(img_folder, self.file_extension)
        else:
            notice.message('Error', messages.ERROR_DICOM)
            return

        notice.message('messages..', '파일 변환이 완료 되었습니다. 아래 Yes 를 눌러 주세요!')

    # mark - Event method
    def loadButtonClicked(self):
        print('call Menu: loadButtonClicked')
        # 사용자가 선택한 파일경로
        file_path = file_manager.file_open()

        if file_path is 0:
            return

        # 사용자가 선택한 파일이름
        last_name = file_path[file_path.rfind('/') + 1:]
        _, fileExtension = os.path.splitext(last_name)
        image_folder = file_path.replace(last_name, '', 1)

        # 확장자 확인
        chioce = fileExtension

        # 썸내일 이미지 만들기
        label_text.check_thumbnail(image_folder)

        # Window 메소드를 호출하여 scroll 에 경로 데이터를 보냅니다.
        call_data = self.call_scroll
        call_data(image_folder, chioce)

    # mark - Event method
    def propertyButtonClicked(self):
        print('call Menu: propertyButtonClicked')
        if self.property_group.isHidden():
            self.property_group.show()
        else:
            self.property_group.hide()

    # mark - Event method
    def exportButtonClicked(self):
        print('call Menu: exportButtonClicked')
        call = self.call_export
        call()

    # mark - Event method
    def algorithmButtonClicked(self):
        print('call Menu: algorithmButtonClicked')
        call = self.call_algorithm
        call()
