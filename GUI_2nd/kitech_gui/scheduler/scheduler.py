import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler

import kitech_gui.gui.gui
from kitech_gui.model import model, representation
from kitech_gui.scheduler import directory

class WeldingScheduler(BackgroundScheduler):
    MODEL = 'kitech_binary.h5'

    def __init__(self, GUI:kitech_gui.gui.gui.GUI):
        super().__init__(timezone='Asia/Seoul')
        self.GUI = GUI
        self.represent = representation.representation()
        self.cnn_model = model.Model(self.MODEL)
        self.dir = directory.Directory()
        self._total = 0
        self._normal = 0
        self._abnormal = 0

    def update(self):
        convert = self.represent.transform_2D(self.represent.merge_df(self.dir.search_new_file()), 9000, 28)
        if convert is not None:
            pred = self.cnn_model.predict(convert)
            normal = len(np.where(  pred < 0.5)[0])
            self._total += len(pred)
            self._normal += normal
            self._abnormal += len(pred) - normal
            self.GUI.total_label.setText(str(self._total))
            self.GUI.normal_label.setText(str(self._normal))
            self.GUI.abnormal_label.setText(str(self._abnormal))
            self.dir.create_result_txt(self._total, self._normal)
            for file in self.dir.search_new_file():
                self.GUI.listview.addItem(file)
            self.dir.update_list()
        else:
            print("new file is not detected")