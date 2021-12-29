"""
Created by SungMin Yoon on 2020-04-27..
Copyright (c) 2020 year SungMin Yoon. All rights reserved.
"""
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *
from LAB.config import path
from LAB.config import setting

TITLE_PATH = 'Path'
TITLE_ROI = 'ROI Image'
TITLE_WINDOW = 'Window'
TITLE_MUSCLE = 'Muscle'
TITLE_START = 'Image processing START'
TITLE_END = 'Image processing END'
TITLE_FILTER_CHOICE = 'Filter'
TITLE_THRESHOLD_CHOICE = 'Threshold'
TITLE_MODE = 'Mode'

VALUE_SELECT_IMAGE = ': No select image'
VALUE_DEFAULT_WINDOW = 800
VALUE_DEFAULT_MUSCLE = 0
VALUE_DEFAULT_START = 0
VALUE_DEFAULT_END = 0


class Tool(QHBoxLayout):
    call_expansion = None           # 콜백 메소드 전체화면 버튼
    call_delete_all = None          # 콜백 메소드 ROI 전체 삭제 버튼
    call_radio_threshold = None     # 콜백 라디오 버튼 쓰레숄드 선택
    call_push_filter = None        # 콜백 라디오 버튼 필터 선택
    call_level_window = None        # 콜백 메소드 윈도우
    call_level_muscle = None        # 콜백 메소드 근육
    call_process_start = None       # 콜백 이미지 처리 시작점
    call_process_end = None         # 콜백 이미지 처리 종료점
    call_mode_chk = None            # 콜백 모드버튼 값

    choice_threshold = None         # 사용자 선택 조직
    choice_filter = None            # 사용자 선택 필터
    slider_window = None            # 슬라이더 윈도우
    slider_muscle = None            # 슬라이더 근육
    slider_start = None             # 슬라이더 이미지 처리 시작점
    slider_end = None               # 슬라이더 이미지 처리 종료점

    # 라디오 버튼
    radio_threshold_list = None     # 쓰레숄드 선택 리스트
    button_filter_list = None        # 필터 선택 리스트

    def __init__(self, parent=None):
        super(Tool, self).__init__(parent)

        # Radio 제목
        self.push_title = QLabel()
        self.push_title.setText(TITLE_FILTER_CHOICE)
        self.radio_title = QLabel()
        self.radio_title.setText(TITLE_THRESHOLD_CHOICE)

        # push filter 버튼 생성
        self.button_filter_list = [None for _ in range(len(setting.FILTER))]
        for i in range(0, len(self.button_filter_list)):

            # 세팅에 정해진 이름을 가지고 옵니다.
            name = f'{i+1} {setting.FILTER[i]}'

            # 푸쉬 버튼 생성
            self.button_filter_list[i] = QPushButton(name)
            push: QPushButton = self.button_filter_list[i]
            push.clicked.connect(lambda stat=False, parameter=push:
                                 self.push_event_filter(parameter))

            # 초기 설정
            if i is 0:
                push.setStyleSheet('background-color: lightGreen')

        # Radio threshold 버튼 생성
        self.radio_threshold_list = [None for _ in range(setting.USER_CHOICE_COUNT)]
        for i in range(0, setting.USER_CHOICE_COUNT):
            name = f'{i+1}'

            # 라디오 버튼 생성
            self.radio_threshold_list[i] = QRadioButton(name)
            radio: QRadioButton = self.radio_threshold_list[i]
            radio.clicked.connect(self.radio_event_threshold)

            # 초기 설정
            if i is 0:
                radio.setChecked(True)

        # Tool UI
        self.verticalBox = QVBoxLayout()
        self.top_box = QHBoxLayout()
        self.level_box = QHBoxLayout()
        self.push_box = QHBoxLayout()
        self.radio_box = QHBoxLayout()

        self.slider_box_top = QHBoxLayout()
        self.slider_box_middle = QHBoxLayout()
        self.slider_box_down = QHBoxLayout()
        self.slider_box_floor = QHBoxLayout()

        # MODE
        self.mode_box = QHBoxLayout()
        self.mode_box.setAlignment(Qt.AlignLeft)

        self.full_screen_box = QHBoxLayout()
        self.delete_all_box = QHBoxLayout()

        self.title_label = QLabel(TITLE_PATH)
        self.title_count = QLabel(TITLE_ROI)

        self.title_mode = QLabel(TITLE_MODE)
        self.title_mode.setGeometry(0, 0, 5, 5)

        self.select_label = QLabel(VALUE_SELECT_IMAGE)

        # ROI 해재 버튼
        self.delete_label = QLabel('Refresh')
        self.delete_btn = QPushButton()
        self.delete_btn.setGeometry(0, 0, 50, 50)
        self.delete_btn.setIcon(QIcon(path.UI_BTN_RED))
        self.delete_btn.setIconSize(QSize(20, 20))
        self.delete_btn.clicked.connect(self.roi_delete_clicked)
        self.delete_btn.setChecked(True)

        # Full screen 버튼
        self.full_screen_label = QLabel('Full screen')
        self.full_screen_btn = QPushButton()
        self.full_screen_btn.setGeometry(0, 0, 50, 50)
        self.full_screen_btn.setIcon(QIcon(path.UI_BTN_GREEN))
        self.full_screen_btn.setIconSize(QSize(20, 20))
        self.full_screen_btn.clicked.connect(self.full_screen_button_clicked)
        self.full_screen_btn.setChecked(True)

        # MODE ROI 버튼
        self.mode_roi_btn = QPushButton()
        self.mode_roi_btn.setText('ROI')
        self.mode_roi_btn.setGeometry(0, 0, 50, 50)
        self.mode_roi_btn.setIconSize(QSize(20, 20))
        self.mode_roi_btn.setChecked(True)
        self.mode_roi_btn.setStyleSheet('background-color: lightGreen')
        self.mode_roi_btn.clicked.connect(lambda stat=False, parameter=0:
                                          self.mode_event(parameter))

        # MODE ZOOM 버튼
        self.mode_zoom_btn = QPushButton()
        self.mode_zoom_btn.setText('ZOOM')
        self.mode_zoom_btn.setGeometry(0, 0, 50, 50)
        self.mode_zoom_btn.setIconSize(QSize(20, 20))
        self.mode_zoom_btn.setChecked(False)
        self.mode_zoom_btn.clicked.connect(lambda stat=False, parameter=1:
                                           self.mode_event(parameter))

        # Level Window
        self.window_label = QLabel(' : level')

        # Level Muscle
        self.muscle_label = QLabel(' : level')

        # process start & end
        self.start_process_label = QLabel(' : number')
        self.end_process_label = QLabel(' : number')

        # 슬라이더 라벨 생성
        window_value_str = f'{VALUE_DEFAULT_WINDOW}'
        muscle_value_str = f'{VALUE_DEFAULT_MUSCLE}'
        start_value_str = f'{VALUE_DEFAULT_START}'
        end_value_str = f'{VALUE_DEFAULT_END}'

        self.label_title_window = QLabel(TITLE_WINDOW)
        self.label_title_muscle = QLabel(TITLE_MUSCLE)
        self.label_title_start = QLabel(TITLE_START)
        self.label_title_end = QLabel(TITLE_END)

        self.label_value_window = QLabel(window_value_str)
        self.label_value_muscle = QLabel(muscle_value_str)
        self.label_value_start = QLabel(start_value_str)
        self.label_value_end = QLabel(end_value_str)

        # 슬라이더 생성
        self.slider_window = QSlider(Qt.Horizontal, None)
        self.slider_window.move(100, 2000)
        self.slider_window.setRange(100, 2000)
        self.slider_window.setSingleStep(1)
        self.slider_window.setValue(VALUE_DEFAULT_WINDOW)
        self.slider_window.valueChanged.connect(self.showWindowSliderValue)

        self.slider_muscle = QSlider(Qt.Horizontal, None)
        self.slider_muscle.move(0, 1000)
        self.slider_muscle.setRange(0, 1000)
        self.slider_muscle.setSingleStep(1)
        self.slider_muscle.setValue(VALUE_DEFAULT_MUSCLE)
        self.slider_muscle.valueChanged.connect(self.showMuscleSliderValue)

        self.slider_start = QSlider(Qt.Horizontal, None)
        self.slider_start.move(0, 1000)
        self.slider_start.setRange(0, 1000)
        self.slider_start.setSingleStep(1)
        self.slider_start.setValue(0)
        self.slider_start.valueChanged.connect(self.showStartSliderValue)

        self.slider_end = QSlider(Qt.Horizontal, None)
        self.slider_end.move(0, 1000)
        self.slider_end.setRange(0, 1000)
        self.slider_end.setSingleStep(1)
        self.slider_end.setValue(0)
        self.slider_end.valueChanged.connect(self.showEndSliderValue)

        self.ui_setup()

    def ui_setup(self):
        # Mount to Widget
        self.top_box.setAlignment(Qt.AlignLeft)
        self.top_box.addWidget(self.title_label, alignment=Qt.AlignLeft)
        self.top_box.addWidget(self.select_label, alignment=Qt.AlignLeft)

        # 라디오 필터 선택 버튼
        self.push_box.addWidget(self.push_title, alignment=Qt.AlignLeft)
        for i in range(0, len(self.button_filter_list)):
            self.push_box.addWidget(self.button_filter_list[i], alignment=Qt.AlignLeft)

        # 라디오 쓰레숄드 선택 버튼
        self.radio_box.addWidget(self.radio_title, alignment=Qt.AlignLeft)
        for i in range(0, len(self.radio_threshold_list)):
            self.radio_box.addWidget(self.radio_threshold_list[i], alignment=Qt.AlignLeft)

        # 슬라이드
        self.slider_box_top.addWidget(self.label_title_window)
        self.slider_box_top.addWidget(self.slider_window)
        self.slider_box_top.addWidget(self.label_value_window)
        self.slider_box_top.addWidget(self.window_label)

        self.slider_box_middle.addWidget(self.label_title_muscle)
        self.slider_box_middle.addWidget(self.slider_muscle)
        self.slider_box_middle.addWidget(self.label_value_muscle)
        self.slider_box_middle.addWidget(self.muscle_label)

        self.slider_box_down.addWidget(self.label_title_start)
        self.slider_box_down.addWidget(self.slider_start)
        self.slider_box_down.addWidget(self.label_value_start)
        self.slider_box_down.addWidget(self.start_process_label)

        self.slider_box_floor.addWidget(self.label_title_end)
        self.slider_box_floor.addWidget(self.slider_end)
        self.slider_box_floor.addWidget(self.label_value_end)
        self.slider_box_floor.addWidget(self.end_process_label)

        # 모드
        self.mode_box.addWidget(self.title_mode, alignment=Qt.AlignLeft)
        self.mode_box.addWidget(self.mode_roi_btn)
        self.mode_box.addWidget(self.mode_zoom_btn)

        # roi 해제 버튼 등록
        self.delete_all_box.addWidget(self.delete_label, alignment=Qt.AlignRight)
        self.delete_all_box.addWidget(self.delete_btn, alignment=Qt.AlignRight)
        self.push_box.addLayout(self.delete_all_box)

        # 풀 스크린 버튼 등록
        self.full_screen_box.addWidget(self.full_screen_label, alignment=Qt.AlignRight)
        self.full_screen_box.addWidget(self.full_screen_btn, alignment=Qt.AlignRight)
        self.radio_box.addLayout(self.full_screen_box)

        # 최상단 툴 박스에 레이아웃 등록
        self.verticalBox.addLayout(self.top_box)
        self.verticalBox.addLayout(self.push_box)
        self.verticalBox.addLayout(self.radio_box)
        self.verticalBox.addLayout(self.slider_box_top)
        self.verticalBox.addLayout(self.slider_box_middle)
        self.verticalBox.addLayout(self.slider_box_down)
        self.verticalBox.addLayout(self.slider_box_floor)
        self.verticalBox.addLayout(self.mode_box)
        self.addLayout(self.verticalBox)

    # mark - Event method
    def radio_event_threshold(self):
        print('Tool: radio_event_threshold')

        for i in range(0, len(self.radio_threshold_list)):
            btn_t: QRadioButton = self.radio_threshold_list[i]

            if btn_t.isChecked() is True:
                self.choice_threshold = i
            else:
                btn_t: QRadioButton = self.radio_threshold_list[i]
                btn_t.setChecked(False)

        call = self.call_radio_threshold
        call(self.choice_threshold)

    # mark - Event method
    def push_event_filter(self, sender):
        print('Tool: radio_event_filter')

        # 전체 버튼 색을 회색으로 바꾸고
        for i in range(0, len(self.button_filter_list)):
            btn_f: QPushButton = self.button_filter_list[i]
            btn_f.setStyleSheet("background-color: lightGray")

        # 사용자 클릭 버튼은 초록색 으로 변경
        btn: QPushButton = sender
        btn.setStyleSheet("background-color: lightGreen")

        # 스트링을 인트형 으로 바꾸고
        new_string = btn.text()
        new_string = new_string[:1]
        int_value = int(new_string)

        # 콜백으로 사용자 선택 필터를 보냄
        self.choice_filter = int_value - 1
        call = self.call_push_filter
        call(self.choice_filter)

    # mark - Event method
    def showWindowSliderValue(self):
        self.label_value_window.setText(str(self.slider_window.value()))
        call = self.call_level_window
        call(self.slider_window.value())

    # mark - Event method
    def showMuscleSliderValue(self):
        self.label_value_muscle.setText(str(self.slider_muscle.value()))
        call = self.call_level_muscle
        call(self.slider_muscle.value())

    # mark - Event method
    def showStartSliderValue(self):
        self.label_value_start.setText(str(self.slider_start.value()))
        call = self.call_process_start
        call(self.slider_start.value())

    def showEndSliderValue(self):
        self.label_value_end.setText(str(self.slider_end.value()))
        call = self.call_process_end
        call(self.slider_end.value())

    # mark - Event method
    def full_screen_button_clicked(self):
        print('tool: full_screen_button_clicked')
        call = self.call_expansion
        call()

    # mark - Event method
    def roi_delete_clicked(self):
        print('tool: roi_delete_clicked')
        call = self.call_delete_all
        call()

    # mark - Event method
    def mode_event(self, value):

        # 모드 번튼 색 변경
        if value == 1:
            self.mode_roi_btn.setStyleSheet("background-color: lightGray")
            self.mode_zoom_btn.setStyleSheet("background-color: lightGreen")
        if value == 0:
            self.mode_roi_btn.setStyleSheet("background-color: lightGreen")
            self.mode_zoom_btn.setStyleSheet("background-color: lightGray")

        # 모드 버튼 선택 값 내보내기
        call = self.call_mode_chk
        call(value)

    # mark - Call back method: window_method
    def set_slider_window(self, value):
        self.slider_window.setValue(value)

    # mark - Call back method: window_method
    def set_slider_muscle(self, value):
        self.slider_muscle.setValue(value)

    # mark - Call back method: window_method
    def set_select_image(self, value):
        index = f': {value}'
        self.select_label.setText(index)
