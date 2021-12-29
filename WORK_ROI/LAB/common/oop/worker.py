"""
Created by SungMin Yoon on 2021-10-18..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
from PySide6.QtCore import QThread, SIGNAL


class Worker(QThread):

    def __init__(self, proc):
        super().__init__()
        self.proc = proc

    # 진행바 쓰레드
    def bar(self, x):
        print('Worker: run')
        self.emit(SIGNAL(self.proc(x)))

