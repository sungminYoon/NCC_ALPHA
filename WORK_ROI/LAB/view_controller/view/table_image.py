"""
Created by SungMin Yoon on 2020-04-07..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from LAB.common.model.info import Info


class TableImage:
    table_list = None       # 테이블 뷰에 보여질 이미지들 리스트 입니다.
    top_widget = None       # 최상단 cell 객체 입니다.
    top_layout = None       # 최상단 cell 의 레이아웃 입니다.
    group_layout = None     # 셀 안의 객체들 입니다.
    call_back = None        # 윈도우 뷰에 선택한 Table mounting data 를 보냅니다.

    def __init__(self):
        pass

    def create(self, data_list):

        # 객체 생성
        self.top_widget = QWidget()
        self.top_layout = QVBoxLayout()
        self.table_list = data_list

        i = 0
        for obj in data_list:
            # 버튼에 표시 되는 숫자 1부터
            index = f'{i+1}'

            # 데이터 모델 타입으로 형변환 합니다.
            data: Info = obj

            # 스크롤 박스에 장착될 그룹 박스
            group_box = QGroupBox()
            group_box.setTitle(data.image_name)
            self.group_layout = QHBoxLayout(group_box)

            # 그룹박스 레이아웃에 들어가는 버튼
            push_button = QPushButton(group_box)
            push_button.setText(index)
            push_button.clicked.connect(lambda stat=False, idx=i: self.click_event(idx))
            push_button.setFixedSize(50, 50)
            self.group_layout.addWidget(push_button)

            # 그룹박스 레이아웃에 들어갈 썸네일 이미지
            thumbnail_path = data.image_thumbnail
            thumbnail = QPixmap(thumbnail_path)
            thumbnail_label = QLabel()
            thumbnail_label.setPixmap(thumbnail)
            thumbnail_label.setGeometry(0, 0, 50, 50)
            self.group_layout.addWidget(thumbnail_label)

            # 스크롤의 가장 위에 보여질 그룹박스
            self.top_layout.addWidget(group_box)
            self.top_widget.setLayout(self.top_layout)

            # 증감
            i = i + 1

    # mark - Event call back Method
    def click_event(self, num):
        print('TableImage: click_event')
        # 실제 리스트에서 가져 올때는 0부터 가져오기 때문에 -1
        data: Info = self.table_list[num]
        path = data.image_path

        # DATA 에서 path 받아 콜백 인자로 처리 합니다.
        call = self.call_back
        call(path, num)

