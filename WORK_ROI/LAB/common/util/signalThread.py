"""
Created by SungMin Yoon on 2021-12-23..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""

from PySide6.QtCore import QThread, SIGNAL
import time


class SignalThread(QThread):

    def __init__(self, proc):
        super().__init__()
        self.proc = proc
        self.count = 0

    def run(self):
        print('Thread: run -> ', self.count)

        while True:
            # 호출 클래스에서 넘겨받은 함수를 수신부로 지정하고 값을 송신한다.
            self.emit(SIGNAL(self.proc(self.count)))
            time.sleep(0.05)



