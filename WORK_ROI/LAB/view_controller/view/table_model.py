"""
Created by SungMin Yoon on 2021-12-16..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from LAB.config import setting
from LAB.config.path import file_manager
from LAB.common.util import notice


class TableModel:

    # table UI
    top_widget = None
    top_layout = None

    # table CELL UI
    push_btn = None
    name_label = None
    info_label = None
    check_box = None

    def __init__(self):
        print('TableModel: init')

        # 위젯 생성
        self.top_widget = QWidget()
        self.top_layout = QVBoxLayout()

        #
