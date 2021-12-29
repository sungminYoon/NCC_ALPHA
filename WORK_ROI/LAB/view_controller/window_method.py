"""
Created by SungMin Yoon on 2021-06-07..
Copyright (c) 2021 year NCC (National Cancer Center). All rights reserved.
"""

import copy
import time

from LAB.common.util import notice
from LAB.common.util import img_text
from LAB.common.util import json_parser
from LAB.config.path import file_manager
from .window_ui import Window

'''
    window_ui 의 
    method 클레스 입니다. 
    ui 의 method 들이 구현 되어 있습니다.
'''


class Window_method(Window):

    def __init__(self, parent=None):
        super(Window_method, self).__init__(parent)
        print('Window_method: init')

    # mark -  Call back method: table_label -> save
    def get_active_path(self):
        return self.active_path

    # mark -  Call back method: table_label -> save
    def get_active_index(self):
        return self.active_image_index

    # mark -  Call back method: table_label -> save
    def get_window(self):
        return self.level_window_value

    # mark -  Call back method: table_label -> save
    def get_muscle(self):
        return self.level_muscle_value

    # mark -  Call back method: tool
    def mode_chk(self, value):
        self.view_main.update_screen()
        self.view_main.mode = value

    # mark -  Call back method: menu
    def algorithm(self):
        print('Window_method: algorithm')

        # 자동처리 준비
        self.auto.clean()
        self.result_list.clear()

        # 사용자 선택 쓰레숄드 마스크들 을 roi 로 생성 합니다.
        masks = self.view_main.get_mask_list()
        self.auto.create_roi(masks)
        if masks[0] is None:
            notice.message('Error', 'Data 가 없습니다. ROI 선택 후 Algorithm 처리를 해주세요!')
            return 0
        else:
            notice.message('알고리즘 처리를 시작합니다!', '잠시만 기다려 주세요! \n처리진행 중 창을 클릭하면 진행바가 멈춥니다!')

        # cv 이미지 들을 가져 옵니다.
        cv_images = self.input_cv_list

        # open cv 이미지들을 처리 메쏘드에 입력 합니다.
        try:
            result, group = self.auto.process_roi(cv_images, self.start_value, self.end_value, self.active_image_index)
        except TypeError:
            print('Window_method: algorithm -> TypeError')
            notice.message('Error 처리를 완료 하지 못했습니다.',
                           '빨간색 Refresh 버튼을 누른 후 \n '
                           'ROI 제 선택과 "Muscle" 조정 후 \n '
                           'Image processing START, END 간격을 조절 해 주세요!')
            return

        self.result_list = result
        self.export_list = group

        # 결과를 테이블에 입력합니다.
        self.table_mask.create(result, self.auto.color_list)

        # 처리결과를 화면 테이블에 보여 줍니다.
        self.scroll_table_mask.setWidget(self.table_mask.top_widget)
        self.scroll_table_mask.show()

        self.progress_value(100, 100)

        time.sleep(1)

        notice.message('알림!', '영상 처리가 완료 되었습니다. \n '
                              '다른 이미지 처리를 원하시면 Refresh 후 진행 하세요!')

    # mark -  Call back method: menu
    def mask_export(self):
        print('Window_method: mask_export')
        if len(self.export_list) < 1:
            notice.message('Error', 'Data 가 없습니다. \n ROI 선택 후 Algorithm 처리를 해주세요!')
            return 0

        notice.message('알림', '잠시만 기다려 주세요! \n 내보내기를 시작합니다.')
        folder = file_manager.folder_name(self.active_path)

        # 날짜 이름을 가진 폴더를 생성 합니다.
        day_folder = file_manager.make_folder(folder)

        # 사용자 선택 마스크 테이블 리스트와 비교
        # img_text.list_compare(self.export_list, self.table_mask.user_select_list)

        # 내보내기 리스트 그룹 풀어놓기
        one_dimension = img_text.to_1_dimension(self.export_list)

        # 마스크를 바이너리로 변환 합니다.
        img_text.to_binary_loop(day_folder, one_dimension)

        # 마스크를 좌표로 변환 합니다.
        json_parser.mask_position_save_text(day_folder, self.table_mask.contour_list)

        msg = f'위치: {day_folder} 에 폴더를 생성 했습니다. 완료!'
        notice.message('알림', msg)

    # mark -  Call back method: menu
    def threshold_input(self, update):
        self.view_main.threshold = int(update)

    # mark -  Call back method: menu
    def threshold_max(self, update):
        self.auto.level_logic.max_size = int(update)
        self.auto.roi_logic.max_size = int(update)

    # mark -  Call back method: menu
    def threshold_min(self, update):
        self.auto.level_logic.min_size = int(update)
        self.auto.roi_logic.min_size = int(update)

    # mark -  Call back method: menu
    def scroll_data(self, img_folder, extension):
        print('Window_method: scroll_data')

        # 필터 저장 리스트 초기화
        self.filter.save_img_list = None

        # 공급자 클래스의 데이타 생성
        self.provider.info_list = []
        self.provider.create(img_folder, extension)
        self.provider.data_read()

        # 테이블에 데이터 넣기
        self.table_img.create(self.provider.info_list)
        self.scroll_table_img.setWidget(self.table_img.top_widget)

        # ui - tool 의 slider_start 범위를 설정합니다.
        self.tool.slider_start.setRange(0, len(self.provider.img_container))
        self.tool.slider_end.setRange(0, len(self.provider.img_container))

        if self.end_value is None:
            self.end_value = len(self.provider.img_container)
        self.tool.label_value_end.setText(f'{self.end_value}')

        # 인풋 리스트에 생성한 이미지를 공급합니다.
        self.input_cv_list = self.provider.img_container

        # 테이블 라벨을 세팅 합니다.
        self.table_label.json_auto_read(img_folder)
        self.scroll_table_label.setWidget(self.table_label.top_widget)

    # mark -  Call back method: tool
    def tool_radio_threshold(self, chk_number):
        print('Window_method: tool_radio')
        self.view_main.user_threshold_change(chk_number)

    def tool_radio_filter(self, chk_number):
        print('Window_method: tool_radio_filter')

        if self.active_image_index is None:
            notice.message('알림', '선택된 이미지가 없습니다. \n 이미지를 먼저 로드 후 선택해 주세요!')

            # 라디오 버튼 초기값으로 되돌리기
            self.filter_check_number = 0
            self.tool.radio_filter_revert()
            return
        else:
            notice.message('알림', '필터 처리를 시작 합니다.')

        # 체크된 필터를 기억 합니다.
        self.filter_check_number = chk_number

        # 공급자에서 cv 이미지 들을 가져 옵니다.
        cv_images = self.provider.img_container

        # 무수정 이미지 리스트 저장
        if self.filter.save_img_list is None:
            print('window_method: tool_radio_filter -> ', self.filter.save_img_list)
            self.filter.save_img_list = copy.deepcopy(cv_images)

        # 필터 처리를 진행 합니다.
        filter_img_list = self.filter.choice(chk_number, cv_images)

        # 필터 처리된 이미지 리스트를 저장하고 리셋합니다.
        self.input_cv_list = filter_img_list
        self.re_setting(self.active_path, self.active_image_index)

        notice.message('알림', '필터 처리가 완료 되었습니다.')

    # mark -  Call back method: tool
    def data_set(self):
        dicom_folder = self.file_open()
        if dicom_folder is '':
            return
        self.provider.create_dicom(dicom_folder)

    # mark -  Call back method: tool
    def screen_expansion(self):
        # UI 스크롤 숨기거나 스크린 확장
        print('Window_method: screen_expansion')

        if self.scroll_table_mask.isHidden() is True:
            self.scroll_table_mask.show()
            self.showFullScreen()
            self.tool.full_screen_btn.setCheckable(True)
        else:
            self.scroll_table_mask.hide()
            self.showNormal()
            self.tool.full_screen_btn.setCheckable(False)

        self.repaint()

    # mark -  Call back method: tool
    def clean_roi(self):
        print('Window_method: clean_roi')

        # 진행바 초기화
        self.progress_bar.setValue(0)

        # 선택한 roi, mask clean
        view_mask_list: list = self.view_main.get_mask_list()
        for obj in view_mask_list:
            if None is obj:
                pass
            else:
                # 객체들을 초기화 합니다.
                self.view_main.clean_mask()
                self.view_main.clean_mouse()
                self.auto.clean()
                self.export_list.clear()
                self.result_list.clear()
                self.re_setting(self.active_path, self.active_image_index)
                self.table_label.create(self.view_main.get_mouse_list(), None)
                self.scroll_table_label.setWidget(self.table_label.top_widget)
                return

    # mark - Call back method: tool
    def level_window(self, value):
        print('Window_method: level_window')

        if self.view_main.screen_img is None:
            return

        # 사용자 UI TOOL 조절 윈도우 레벨을 업데이트 합니다.
        self.auto.level_window = value
        self.level_window_value = value
        self.view_main.level_window = value
        self.view_main.level_muscle = self.level_muscle_value
        self.view_main.update_level()

    # mark - Call back method: tool
    def level_muscle(self, value):
        print('Window_method: level_muscle')

        if self.view_main.screen_img is None:
            return

        # 사용자 UI TOOL 조절 근육 레벨을 업데이트 합니다.
        self.auto.level_muscle = value
        self.level_muscle_value = value
        self.view_main.level_window = self.level_window_value
        self.view_main.level_muscle = value
        self.view_main.update_level()

    # mark - Call back method: tool
    def start_point(self, value):
        print('Window_method: start_point')
        if self.view_main.screen_img is None:
            notice.message('선택된 이미지가 없습니다.', '이미지를 먼저 Load 후 선택해 주세요!')
            return

        # 사용자 지정 처리 이미지 시작점
        self.start_value = value

    # mark - Call back method: tool
    def end_point(self, value):
        print('Window_method: end_point')

        # 사용자 지정 처리 이미지 종료점
        self.end_value = value









