"""
Created by SungMin Yoon on 2021-07-19..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import os
import copy
import json

from datetime import datetime
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from LAB.config import setting
from LAB.config.path import file_manager
from LAB.common.util import notice

BOX_SIZE_WIDTH = 512
BOX_SIZE_HEIGHT = 150
CELL_SIZE_WIDTH = 135
CELL_SIZE_HEIGHT = 30


class TableLabel:

    # 사용자 선택 값, 경로 가져오기
    call_path = None
    call_index = None
    call_window = None
    call_muscle = None

    # 테이블 의 정보를 뷰로 보냅니다.
    call_load_view = None

    # 사용자 쓰레숄드 좌표 리스트
    user_mouse_position_list = None

    # 사용자 텍스트 입력 값.
    user_input_list = None

    # 읽어드린 JSON 데이타
    json_data = None

    # 하위 json list
    elements_list = None

    # table UI
    top_widget = None
    top_layout = None

    # table CELL UI
    label_number = None
    label_info_list = None
    line_edit_list = None
    group_box_list = None
    info_box_list = None

    def __init__(self):
        self.user_mouse_position_list = []
        self.elements_list = []

        # CELL UI
        self.user_input_list = [None for _ in range(setting.USER_CHOICE_COUNT)]
        self.label_info_list = [QLabel() for _ in range(setting.USER_CHOICE_COUNT)]
        self.line_edit_list = [QLineEdit() for _ in range(setting.USER_CHOICE_COUNT)]
        self.group_box_list = [QGroupBox() for _ in range(setting.USER_CHOICE_COUNT)]
        self.info_box_list = [QVBoxLayout() for _ in range(setting.USER_CHOICE_COUNT)]

        # 위젯 생성
        self.top_widget = QWidget()
        self.top_layout = QVBoxLayout()

        # Select image Label
        self.label_number = QLabel()

        # load button
        load_btn = QPushButton()
        load_btn.setText(f'LOAD')
        load_btn.clicked.connect(lambda stat=False, parameter=0:
                                 self.click_load_json(parameter))

        # save button
        save_btn = QPushButton()
        save_btn.setText(f'SAVE')
        save_btn.clicked.connect(lambda stat=False, parameter=1:
                                 self.click_save_label(parameter))

        # layout box
        top_group = QVBoxLayout()
        top_box = QHBoxLayout()
        top_chile = QVBoxLayout()
        top_box.addWidget(load_btn)
        top_box.addWidget(save_btn)
        top_chile.addWidget(self.label_number)
        top_group.addLayout(top_box)
        top_group.addLayout(top_chile)

        # 스크롤의 가장 위에 보여질 그룹박스
        self.top_layout.addLayout(top_group)

    def clear(self):
        self.user_mouse_position_list.clear()
        self.elements_list.clear()

    # 테이블 라벨을 생성 합니다.
    def create(self, mouse_list, user_select_number):
        print('TableLabel: create')

        # 준비
        if user_select_number is None:
            user_select_number = 0
        user_int: int = int(user_select_number)
        self.user_mouse_position_list = copy.copy(mouse_list)
        self.label_number.setText(f'   Select image : {user_int + 1}')

        # 사용자 선택 이미지가 없으면 입력도 초기화 합니다.
        if user_select_number is None:
            self.user_input_list = [None for _ in range(setting.USER_CHOICE_COUNT)]

        # 사용자 memo 가 없다면 "input" 단어을 넣어 줍니다.
        if self.user_input_list is None:
            self.user_input_list = ['input' for _ in range(setting.USER_CHOICE_COUNT)]

        for i in range(0, len(mouse_list)):
            obj = mouse_list[i]

            # info Label
            self.label_info_list[i].setText(f'position xy: {obj}')

            # Line edit (텍스트 입력 박스)
            self.line_edit_list[i].setObjectName(f'{i}')
            self.line_edit_list[i].setText(self.user_input_list[i])
            self.setting_line_edit(self.line_edit_list[i])

            # 정보를 표시한 라벨과 텍스트 입력창을 넣어 줍니다.
            self.info_box_list[i].addWidget(self.label_info_list[i])
            self.info_box_list[i].addWidget(self.line_edit_list[i])

            # 스크롤 박스에 장착될 그룹 박스
            self.group_box_list[i].setMaximumWidth(BOX_SIZE_WIDTH)
            self.group_box_list[i].setMaximumHeight(BOX_SIZE_HEIGHT)
            self.group_box_list[i].setTitle(f'[{i+1}]')
            self.group_box_list[i].setLayout(self.info_box_list[i])

            # 스크롤의 가장 위에 보여질 그룹박스
            self.top_layout.addWidget(self.group_box_list[i])
            self.top_widget.setLayout(self.top_layout)

            # 증감
            i = i + 1

    # mark -  Event method
    # JSON 파일을 가져 옵니다.
    def click_load_json(self, parameter):
        print('TableLabel: click_load_json', parameter)

        # 사용자 입력 텍스트 초기화
        self.user_input_list = [None for _ in range(setting.USER_CHOICE_COUNT)]

        # 사용자 선택 json 파일
        file_path = file_manager.file_open()
        filename = os.path.splitext(file_path)[1]

        if filename in '.json':

            # json 파일을 읽어 반환 합니다.
            with open(file_path, 'r') as f:
                self.json_data = json.load(f)
                self.json_parsing()
        else:
            notice.message('Error', 'Json 파일을 선택해 주세요!')

    # mark -  Event method
    # JSON 파일을 저장 합니다.
    def click_save_label(self, parameter):
        print('TableLabel: click_save_label', parameter)

        # json 그룹을 만듭니다.
        img_group = dict()

        if self.call_index() is None:
            notice.message('Error', '좌측 테이블 이미지를 선택해 주세요!')
            return 0

        # 사용자 선택한 무수정 이미지 번호 입니다.
        user_choice_img_number = int(self.call_index())
        user_choice_img_number = user_choice_img_number + 1
        img_number = f'{user_choice_img_number}'
        count = len(self.user_mouse_position_list)

        # 활성화된 img 경로를 가지고 옵니다.
        path = self.call_path()
        window = self.call_window()
        muscle = self.call_muscle()

        # json 그룹속에 key 와 value 를 만듭니다.
        img = dict()
        img["number"] = img_number
        img["count"] = count
        img["window"] = window
        img["muscle"] = muscle
        img["path"] = path
        img_group["img"] = img

        # 테이블 길이 만큼 반복합니다.
        for j in range(0, len(self.user_mouse_position_list)):

            # 테이블 리스트의 마우스 포지션 객체를 가저옵니다.
            obj = self.user_mouse_position_list[j]

            # json 생성하고
            position = dict()

            # position 데이터가 없으면 0
            if obj is None:
                position["x"] = 0
                position["y"] = 0

            # position 데이터가 있으면 저장
            else:
                _x = f'{obj[0]}'
                _y = f'{obj[1]}'
                position["x"] = _x
                position["y"] = _y

            # 사용자 입력 텍스트
            _input = self.user_input_list[j]

            # 마스크 정보를 저장할 json 을  생성.
            threshold_info = dict()

            # json 의 key 에 value 를 저장 합니다.
            threshold_info["memo"] = _input
            threshold_info["position"] = position

            # json 으로 만든 데이터를 리스트에 저장합니다.
            self.elements_list.append(threshold_info)

        # 테이블 길이만큼 반복합니다.
        for j in range(0, len(self.user_mouse_position_list)):

            # json 최상위 그룹에 json 리스트를 저장합니다.
            _name = f'mask_{j + 1}'
            _json = self.elements_list[j]
            img_group[_name] = _json

        # 파일 이름을 날짜, 시간 으로 만듭니다.
        folder_path = file_manager.folder_name(path)
        file_name = datetime.today().strftime("%Y%m%d%H%M%S")
        file_extension = f'.json'
        file_path = f'{folder_path}{file_name}{file_extension}'

        # 파일 경로, 이름을 가지고 json 형식으로 저장 합니다.
        with open(file_path, 'w', encoding='utf-8') as make_file:
            json.dump(img_group, make_file, indent="\t")

        msg = f'위치: {file_path} TEXT 저장이 완료 되었습니다.'
        notice.message('알림', msg)
        self.clear()

    # mark -  Event method
    # 텍스트 입력 박스를 세팅 합니다.
    def setting_line_edit(self, q_line: QLineEdit):
        q_line.setAlignment(Qt.AlignRight)
        q_line.setFixedWidth(CELL_SIZE_WIDTH)
        q_line.setFixedHeight(CELL_SIZE_HEIGHT)

        # 입력 할 때 마다 호출
        q_line.textChanged.connect(lambda stat=False, parameter=q_line:
                                   self.lineChanged(parameter))

    # mark - Event method
    # 글이 입력될 때 마다 호출 됩니다.
    def lineChanged(self, sender):
        print('TableLabel: lineChanged')

        # sender 을 QLineEdit 변환 합니다.
        line_edit: QLineEdit = sender
        number: int = int(line_edit.objectName())

        # 사용자가 입력한 text 데이터를 list 에 저장 합니다.
        if sender.text() is '':
            print('TableLabel: empty')
        else:
            self.user_input_list[number] = line_edit.text()

    # 자동으로 해당 path json data 를 가지고 옵니다.
    def json_auto_read(self, img_folder):
        print('TableLabel: json_auto_read', img_folder)

        # json 파일 이름 들을 가저 옵니다.
        _json_list = file_manager.file_json_list(img_folder)

        # json 데이터가 없다면
        if len(_json_list) < 1:
            # None 데이터를 생성
            mouse_list = [None for _ in range(setting.USER_CHOICE_COUNT)]
            return self.create(mouse_list, None)

        # 리스트 에서 마지막 json 파일을 가지고 옵니다.
        if len(_json_list) > 0:
            _json = _json_list[-1]
            path = f'{img_folder}{_json}'

            # json 파일을 읽고 파싱 합니다.
            with open(path, 'r') as f:
                self.json_data = json.load(f)
                self.json_parsing()

    # json 데이터를 가공 합니다.
    def json_parsing(self):
        # 초기화
        mouse_position_list = []
        user_memo_list = []
        user_select_image = None

        if self.json_data is None:
            print('TableLabel: json_parsing -> None')
            return 0

        # JSON 의 KEY 와 VALUE 데이터를 가지고 옵니다.
        count = self.json_data["img"]["count"]
        number = self.json_data["img"]["number"]
        window = self.json_data["img"]["window"]
        muscle = self.json_data["img"]["muscle"]
        path = self.json_data["img"]["path"]

        # 사용자 마스크 개수 만큼 반복 합니다.
        for i in range(0, count):
            key = f'mask_{i+1}'
            x = self.json_data[key]["position"]["x"]
            y = self.json_data[key]["position"]["y"]

            # 값을 가지고 옵니다.
            _position = (x, y)
            _memo = self.json_data[key]["memo"]

            # 값을 저장 합니다.
            mouse_position_list.append(_position)
            user_memo_list.append(_memo)
            user_select_image = number
            self.user_input_list = user_memo_list

        # JSON 에서 저장한 리스트로 라벨 테이블 생성 및 뷰 핸들링
        self.create(mouse_position_list, user_select_image)
        self.view_handling(mouse_position_list,
                           user_select_image,
                           window, muscle,
                           path)

    # 뷰로 테이블 라벨의 정보를 보냅니다.
    def view_handling(self, mouse_position_list,
                      user_select_image,
                      window,
                      muscle,
                      path):

        print('TableLabel: call_load_view')
        call_load_view = self.call_load_view
        call_load_view(user_select_image, mouse_position_list, window, muscle, path)
