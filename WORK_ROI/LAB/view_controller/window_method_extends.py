"""
Created by SungMin Yoon on 2021-11-24..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""
import math
import time

from PySide6.QtGui import *
from .window_method import Window_method

'''
    window_method 의 
    확장(extends) 클레스 입니다. 
    Window 화면의 main view 와 AI 로직을 운전하고 
    진행바 가 구현되어 있습니다.
'''


class Window_method_extends(Window_method):

    def __init__(self, parent=None):
        super(Window_method_extends, self).__init__(parent)
        print('Window_method_extends: init')

    # mark - Call back method: view
    def view_label_update(self, mouse_list):

        # 화면의 중하단 에 표시되는 테이블 라벨을 업데이트 합니다.
        self.table_label.create(mouse_list, self.active_image_index)
        self.scroll_table_label.setWidget(self.table_label.top_widget)

    # mark - Call back method: view
    def view_handling(self, user_select_image, mouse_position_list, window, muscle, path):

        # 사용자 선택, 입력 정보를 이용해 뷰를 동작 시킵니다.
        print('Window_method_extends: view_handling')

        # UI TOOL 표시 설정
        self.tool.set_slider_window(window)
        self.tool.set_slider_muscle(muscle)

        # 화면에 적용되는 값 입력
        self.view_main.level_window = window
        self.view_main.level_muscle = muscle

        # 영상처리에 적용되는 값 입력
        self.auto.level_window = window
        self.auto.level_muscle = muscle

        # 화면 갱신및 마우스 좌표정보 전달
        user_int: int = int(user_select_image)
        self.re_setting(path, user_int - 1)
        self.view_main.set_mouse_list(mouse_position_list)

    # mark -  Call back method: Table_img
    def re_setting(self, path, index):
        print('Window_method_extends: re_setting', path)

        # Table_image 에서 사용자 선택한 path, index 입니다.
        self.active_path = path
        self.active_image_index = index
        self.tool.set_select_image(path)

        # 현재 사용자 선택된 이미지 인덱스 입니다.
        int_index: int = int(index)

        # 메뉴에 사용자 선택된 현재 이미지 넘버.
        current_image_text = f'Select image : {int_index + 1} '
        self.menu.changeLabel(current_image_text)

        # 보여지는 view 에 들어갈 이미지 준비.
        img = self.input_cv_list[int_index]
        h, w = img.shape[:2]
        q_image = QImage(img, w, h, QImage.Format_Grayscale8)
        pix_image = QPixmap.fromImage(q_image)

        # 보여지는 view 에 이미지를 넣어 주고
        self.view_main.q_graphic.setPixmap(pix_image)
        self.view_main.re_setting(img)
        self.view_main.repaint()

    # mark -  Call back method: auto
    def progress_value(self, length, input_value):
        # print('Window_method_extends: progress_value')

        # 진행 값을 퍼센트로 변환 합니다.
        f_value = float((input_value / length) * 100)
        result = math.floor(f_value)

        # 쓰레드를 사용해 진행바를 실행 합니다.
        self.signal_thread.count = result

        time.sleep(0.05)

        if input_value == 100:
            print('progress_bar: STOP')
            self.signal_thread.terminate()

        if input_value == 0:
            print('progress_bar: START')
            self.signal_thread.start()

    # 진행 바 카운트 입니다.
    def proc(self, count):
        self.progress_bar.setValue(count)

    # mark - Call back method: menu
    def ai_answer(self):
        print('Window_method_extends: ai_predict')
        self.ai.answer_data()

    # mark - Call back method: menu
    def ai_training(self):
        print('Window_method_extends: ai_training')
        self.ai.training_data()

    # mark - Call back method: menu
    def ai_analysis(self):
        print('Window_method_extends: ai_analysis')

    # mark - Call back method: menu
    def ai_merge(self):
        print('Window_method_extends: ai_merge')