"""
일정 주기마다 이벤트를 발생시키는 스케줄러 기능 구현. apscheduler의 BackgroundScheduler를 사용.
"""

import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler

import kitech_gui.gui.gui
from kitech_gui.model import model, representation
from kitech_gui.scheduler import directory

class WeldingScheduler(BackgroundScheduler):
    def __init__(self, GUI:kitech_gui.gui.gui.GUI, dir_path:str):
        super().__init__(timezone='Asia/Seoul')
        self.GUI = GUI
        self.represent = representation.representation(dir_path)
        self.cnn_model = model.Model(self.MODEL)
        self.dir = directory.Directory(dir_path)
        self._total = 0
        self._normal = 0
        self._abnormal = 0

    """ 스케줄러 과정 : 새로운 파일 탐색 -> 전처리 및 예측 -> UI 업데이트 -> 결과 txt 파일 생성 -> 내부 값 업데이트 """
    def update(self):
        #preprocessing & predict
        convert = self.represent.transform_2D(self.represent.merge_df(self.dir.search_new_file()), 9000, 28)
        if convert is not None:
            pred = self.cnn_model.predict(convert)
            normal = len(np.where(  pred < 0.5)[0])
            self._total += len(pred)
            self._normal += normal
            self._abnormal += len(pred) - normal

            #gui update
            self.GUI.total_label.setText(str(self._total))
            self.GUI.normal_label.setText(str(self._normal))
            self.GUI.abnormal_label.setText(str(self._abnormal))
            for file in self.dir.search_new_file():
                self.GUI.listview.addItem(file)

            #txt file create
            self.dir.create_result_txt(self._total, self._normal)

            #list update
            self.dir.update_list()
        else:
            print("new file is not detected")