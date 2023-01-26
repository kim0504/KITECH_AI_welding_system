import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from apscheduler.schedulers.qt import QtScheduler
import directory
import representation
import model
import numpy as np

class GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self._total = 0
        self._normal = 0
        self._abnormal = 0
        self.sched = directory.dir_info("../GUI_2nd_temp")  # 수정필요
        self.preprocess = representation.representation()

    def initUI(self):
        total_Hlayout = QHBoxLayout()
        total_Hlayout.addStretch(1)
        total_Hlayout.addLayout(self.total_layout(), stretch=2)
        total_Hlayout.addLayout(self.normal_layout(), stretch=2)
        total_Hlayout.addLayout(self.abnormal_layout(), stretch=2)
        total_Hlayout.addStretch(1)

        total_Vlayout = QVBoxLayout()
        total_Vlayout.addStretch(1)
        total_Vlayout.addLayout(total_Hlayout, stretch=3)
        total_Vlayout.addStretch(1)

        self.setLayout(total_Vlayout)

        self.setWindowTitle('GUI_SYSYTEM')
        self.setGeometry(300, 300, 300, 200)
        self.showMaximized()

    def Qlabel_style(self, name):
        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            "border-style: solid; border-width: 2px; border-color: #dbd9d9; padding:10% 0; background-color: #ffffff")
        font = label.font()
        font.setPointSize(44)
        label.setFont(font)
        return label

    def total_layout(self):
        layout = QVBoxLayout()
        total_title = self.Qlabel_style('Total')
        self.total_label = self.Qlabel_style('-')
        layout.addWidget(total_title)
        layout.addWidget(self.total_label)
        return layout

    def normal_layout(self):
        layout = QVBoxLayout()
        normal_title = self.Qlabel_style('Normal')
        self.normal_label = self.Qlabel_style('-')
        layout.addWidget(normal_title)
        layout.addWidget(self.normal_label)
        return layout

    def abnormal_layout(self):
        layout = QVBoxLayout()
        abnormal_title = self.Qlabel_style('Abnormal')
        self.abnormal_label = self.Qlabel_style('-')
        layout.addWidget(abnormal_title)
        layout.addWidget(self.abnormal_label)
        return layout

    def update(self):
        convert = self.preprocess.transform_2D(self.preprocess.merge_df(self.sched.get_new_file()), 9000, 28)
        if convert is not None:
            pred = model.Model('kitech_binary.h5').predict(convert)
            normal = len(np.where(pred < 0.5)[0])
            self._total += len(pred)
            self._normal += normal
            self._abnormal += len(pred) - normal
            self.total_label.setText(str(self._total))
            self.normal_label.setText(str(self._normal))
            self.abnormal_label.setText(str(self._abnormal))
        else:
            print("new file is not detected")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()

    scheduler = QtScheduler()
    scheduler.add_job(ex.update, 'interval', seconds=20)
    scheduler.start()

    sys.exit(app.exec_())