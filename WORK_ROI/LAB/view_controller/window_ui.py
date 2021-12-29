"""
Created by SungMin Yoon on 2021-06-07..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
from PySide6 import QtCore
from PySide6.QtWidgets import *
from LAB.config import setting
from LAB.common.util.signalThread import SignalThread
from .view.ui_tool import Tool
from .view.ui_menu import Menu
from .view.view_main import ViewMain
from .view.table_image import TableImage
from .view.table_mask import TableMask
from .view.table_label import TableLabel

from .control.auto import Auto
from .control.provider import Provider
from .control.filter import Filter


class Window(QWidget):

    """CONTROL"""
    ai = None                       # ai 예측 처리
    auto = None                     # 자동 이미지 처리
    provider = None                 # 이미지 DATA 공급자
    filter = None                   # 이미지 필터

    """TABLE"""
    scroll_table_img = None         # 좌측 스크롤 테이블 이미지
    scroll_table_mask = None        # 우측 스크롤 2줄 테이블 마스크
    scroll_table_label = None       # 중간 스크롤 테이블 라벨
    table_img = None                # 좌측 이미지 테이블 셀
    table_mask = None               # 우측 2줄 테이블 셀
    table_label = None              # 중간 라벨 테이블 셀

    """TOOL"""
    tool = None                     # 상단 도구 버튼 모음 입니다.
    level_window_value = None       # 화면에 보여지는 뷰의 윈도우 레벨 값
    level_muscle_value = None       # 화면에 보여지는 뷰의 근육 레벨 값
    start_value = None              # 사용자 지정 이미지 처리 시작점
    end_value = None                # 사용자 지정 이미지 처리 종료점
    progress_bar = None             # 진행 바

    """MENU"""
    menu = None                     # 좌측 상단 File Menu 버튼 모음 입니다.

    """VIEW"""
    view_main = None                # 화면에 보여지는 image 뷰 입니다.
    view_second = None              # 화면에 보여지는 Level 뷰 입니다.

    """ACTIVE VALUE"""
    active_path = None          # 뷰에 활성화된 이미지 경로
    active_image_index = None   # 뷰에 활성화된 이미지 인덱스 번호
    filter_check_number = None  # 사용자 선택 필터 번호
    export_list: list = None    # 내보내기 마스크 리스트 입니다.
    input_cv_list: list = None  # 입력되는 cv 이미지 리스트 입니다.

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # 리스트 생성
        self.export_list = []
        self.result_list = []
        self.input_cv_list = []

        # 컨트롤 클래스 생성
        self.auto = Auto()
        self.provider = Provider()
        self.filter = Filter()
        self.filter_check_number = 0

        # 윈도우 세팅
        self.setWindowTitle(setting.TITLE_WINDOW)
        self.setGeometry(0, 0, setting.WINDOW_SCREEN_WIDTH, setting.WINDOW_SCREEN_HEIGHT)

        # View 생성
        self.view_main = ViewMain()
        self.view_main.setup()
        self.view_main.threshold = setting.THRESHOLD

        # 스크롤과 테이블 생성
        self.scroll_table_img = QScrollArea()
        self.scroll_table_mask = QScrollArea()
        self.scroll_table_label = QScrollArea()
        self.table_mask = TableMask()
        self.table_img = TableImage()
        self.table_label = TableLabel()

        # 프로그래스바 생성
        self.progress_bar = QProgressBar(self)
        self.signal_thread = SignalThread(self.proc)
        self.step = 0

        # 메뉴 생성
        self.menu = Menu()

        # 툴 생성
        self.tool = Tool()

        # LEVEL 값 초기화
        self.level_window_value = setting.DEFAULT_LEVEL_WINDOW
        self.level_muscle_value = setting.DEFAULT_LEVEL_MUSCLE

        # Menu 콜백 객체에 Window 메소드를 등록 합니다.
        self.menu.call_scroll = self.scroll_data
        self.menu.call_export = self.mask_export
        self.menu.call_algorithm = self.algorithm
        self.menu.call_answer = self.ai_answer
        self.menu.call_training = self.ai_training
        self.menu.call_analysis = self.ai_analysis
        self.menu.call_merge = self.ai_merge

        # Tool 콜백 객체에 Window 메소드를 등록합니다.
        self.tool.call_data_set = self.data_set
        self.tool.call_expansion = self.screen_expansion
        self.tool.call_delete_all = self.clean_roi
        self.tool.call_level_window = self.level_window
        self.tool.call_level_muscle = self.level_muscle
        self.tool.call_process_start = self.start_point
        self.tool.call_process_end = self.end_point
        self.tool.call_radio_threshold = self.tool_radio_threshold
        self.tool.call_push_filter = self.tool_radio_filter
        self.tool.call_mode_chk = self.mode_chk

        # Auto 콜백 객체에 Window 메소드를 등록 합니다.
        self.auto.call_progress = self.progress_value
        self.auto.max_value = setting.PROPERTY_MIN
        self.auto.min_value = setting.PROPERTY_MAX

        # View 콜백 객체에 Window 메소드를 등록 합니다.
        self.view_main.call_click_threshold = self.view_label_update
        self.view_main.tool_radio_chk = 0

        # Table 콜백 객체에 Window 메소드를 등록 합니다.
        self.table_img.call_back = self.re_setting
        self.table_label.call_path = self.get_active_path
        self.table_label.call_index = self.get_active_index
        self.table_label.call_window = self.get_window
        self.table_label.call_muscle = self.get_muscle
        self.table_label.call_load_view = self.view_handling

        self.ui_setup()

    def ui_setup(self):
        print('ui_setup')

        # 전체폼 박스
        form_box = QHBoxLayout()
        _frame_box = QVBoxLayout()
        _top = QVBoxLayout()
        _left = QVBoxLayout()
        _center = QHBoxLayout()
        _view_box = QVBoxLayout()
        _label_box = QVBoxLayout()
        _right = QVBoxLayout()

        # right hide layout
        ly = QVBoxLayout()

        # 스크롤 뷰 등록
        _right.addWidget(self.scroll_table_mask)
        self.scroll_table_mask.setLayout(ly)
        self.scroll_table_mask.hide()

        # image view 좌측 상단 고정
        self.view_main.setAlignment(QtCore.Qt.AlignTop)
        _view_box.addWidget(self.view_main, alignment=QtCore.Qt.AlignLeft)

        # 스크롤 라벨 테이블 등록
        self.scroll_table_label.setAlignment(QtCore.Qt.AlignLeft)
        _label_box.addWidget(self.scroll_table_label, alignment=QtCore.Qt.AlignLeft)

        # left layout
        _left.addLayout(self.menu)
        _left.addWidget(self.scroll_table_img)

        # top layout
        _top.addLayout(self.tool)
        _top.addWidget(self.progress_bar)

        # 창을 늘여도 왼쪽고정
        _center.setAlignment(QtCore.Qt.AlignLeft)
        _center.addLayout(_view_box)
        _center.addLayout(_label_box)
        _center.addLayout(_right)

        _frame_box.addLayout(_top)
        _frame_box.addLayout(_center)

        # 전체 폼박스에 배치
        form_box.addLayout(_left)
        form_box.addLayout(_frame_box)
        form_box.setStretchFactor(_left, 0)
        form_box.setStretchFactor(_frame_box, 1)

        # 레이아웃에 폼박스 등록
        self.setLayout(form_box)
        self.show()















