"""
Created by SungMin Yoon on 2020-12-08..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
import time
from PySide6.QtCore import QSize
from PySide6.QtGui import *
from PySide6.QtGui import QImage
from PySide6.QtWidgets import *
from LAB.config import path
from LAB.common.util import img_threshold


class TableMask:

    # Table UI 입니다.
    top_widget = None
    top_layout = None
    group_layout = None

    # icon image 세팅 값입니다.
    muscle_value = None
    window_value = None

    # UI 리스트 입니다.
    label_slider_list: list
    level_slider_list: list

    export_list: list           # 내보내기 리스트 입니다.
    contour_list: list          # 내보내기 좌표 리스트 입니다.
    copy_image: list            # icon image 리스트
    user_select_list: list      # 사용자 선택 마스크
    image_button_list: list     # 확인 테이블 뷰에 보여지는 버튼 리스트
    mask_button_list: list      # 확인 테이블 뷰에 보여지는 버튼 리스트

    def __init__(self):
        # 리스트를 생성합니다.
        self.label_slider_list = []
        self.level_slider_list = []
        self.export_list = []
        self.contour_list = []

        self.copy_image = []
        self.user_select_list = []
        self.image_button_list = []
        self.mask_button_list = []

    def list_clear(self):
        # 리스트를 초기화 합니다.
        self.label_slider_list.clear()
        self.level_slider_list.clear()
        self.export_list.clear()
        self.contour_list.clear()

        self.copy_image.clear()
        self.user_select_list.clear()
        self.image_button_list.clear()
        self.mask_button_list.clear()

    def create(self, mask_list, cv_list):
        print('TableMask: create')

        # 다시 생성을 위한 초기화
        self.list_clear()

        # UI 객체 생성
        self.top_widget = QWidget()
        self.top_layout = QVBoxLayout()

        # 테이블 셀 개수만 카운트 해서 어긋남을 방지 합니다.
        table_cell_count = 0

        if mask_list is None:
            print('TableMask: ', mask_list)
            return

        for i in range(0, len(mask_list)):

            if mask_list[i] == 0:
                pass
            else:
                # 마스크 리스트 에서 이미지를 객체를 가져 옵니다.
                image_obj = mask_list[i]

                # 이미지 객체에서 data 를 가져 옵니다.
                level_image, number = image_obj
                h, w = level_image.shape[:2]

                # cv 이미지를 가져 옵니다.
                img = cv_list[number]

                # level 이미지 컨투어 쓰레숄드
                time.sleep(0.1)
                threshold_image, contours = img_threshold.contour_to_bgr(level_image)

                # 이미지 넘버와 이미지에 속한 컨투어 정보를 컨투어 리스트에 저장합니다.
                t = (number, contours)
                self.contour_list.append(t)

                # 스크롤 박스에 장착될 그룹 박스
                group_box = QGroupBox()
                group_box.setMaximumWidth(w * 2)
                group_box.setMaximumHeight(h)
                group_box.setTitle(f'{number+1}')
                self.group_layout = QHBoxLayout(group_box)

                # BGR888 버튼 이미지 세팅
                table_left = QImage(img, w, h, QImage.Format_BGR888)
                table_right = QImage(threshold_image, w, h, QImage.Format_BGR888)

                pix_image = QPixmap.fromImage(table_left)
                pix_mask = QPixmap.fromImage(table_right)

                icon_image = QIcon(pix_image)
                icon_mask = QIcon(pix_mask)

                # number = 테이블 표시 번호 , i = cv 이미지 카운트, 버튼 상태
                t = (f'{number}', True)
                self.user_select_list.append(t)
                self.copy_image.append(icon_image)

                # 이미지 버튼을 생성
                button_left = QPushButton()

                # 이미지 버튼 상태 체크
                button_left.setCheckable(True)

                # 이미지 버튼 세팅
                button_left.setObjectName(f'{table_cell_count}')
                button_left.setGeometry(0, 0, w, h)

                button_left.setIcon(icon_image)
                button_left.setIconSize(QSize(w, h))
                button_left.clicked.connect(lambda stat=False, parameter=table_cell_count:
                                            self.click_event_image(parameter))

                # 리스트와 UI 에 이미지 버튼 등록
                self.image_button_list.append(button_left)
                self.group_layout.addWidget(button_left)

                # 마스크 버튼 생성
                button_right = QPushButton()
                button_right.clicked.connect(lambda stat=False, parameter=table_cell_count:
                                             self.click_event_mask(parameter))
                button_right.setGeometry(0, 0, w, h)
                button_right.setIcon(icon_mask)
                button_right.setIconSize(QSize(w, h))

                # 리스트와 UI 에 마스크 버튼 등록
                self.mask_button_list.append(button_right)
                self.group_layout.addWidget(button_right)

                # 스크롤의 가장 위에 보여질 그룹박스
                self.top_layout.addWidget(group_box)
                self.top_widget.setLayout(self.top_layout)

                # 샐 생성 카운트 증감
                table_cell_count = table_cell_count + 1

    # mark - Event Method
    def click_event_image(self, idx):
        print('TableMask: click_event_mask')
        button: QPushButton = self.image_button_list[idx]

        chk = button.isCheckable()
        if chk is True:
            button.setCheckable(False)
            button.setIcon(QIcon(path.TABLE_CELL_OFF))
            name = button.objectName()
            index = int(name)

            # _1 = 테이블 표시 번호
            # _2 = 버튼 상태
            _1, _2 = self.user_select_list[index]
            print('TableMask = ', _1, _2)
            t = (_1, False)
            self.user_select_list[index] = t

        else:
            button.setCheckable(True)
            name = button.objectName()
            index = int(name)
            image = self.copy_image[index]
            button.setIcon(image)
            _1, _2 = self.user_select_list[index]
            t = (_1, True)
            self.user_select_list[index] = t

    # mark - Event Method
    def click_event_mask(self, idx):
        print('TableMask: click_event_image')
        button: QPushButton = self.mask_button_list[idx]
        index = button.objectName()
        print('TableMask: click_event_image -> index = ', index)

