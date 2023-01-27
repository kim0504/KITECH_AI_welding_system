import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget
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
        self.sched = directory.dir_info("../../GUI_2nd_temp")  # 수정필요
        self.preprocess = representation.representation()

    def initUI(self):
        result_layout = QVBoxLayout()
        result_layout.addLayout(self.total_layout())
        result_layout.addLayout(self.normal_layout())
        result_layout.addLayout(self.abnormal_layout())

        total_Hlayout = QHBoxLayout()
        total_Hlayout.addStretch(1)
        total_Hlayout.addLayout(result_layout, stretch=9)
        total_Hlayout.addStretch(1)
        total_Hlayout.addLayout(self.listview_layout(), stretch=5)
        total_Hlayout.addStretch(1)

        total_Vlayout = QVBoxLayout()
        total_Vlayout.addStretch(1)
        total_Vlayout.addLayout(total_Hlayout, stretch=7)
        total_Vlayout.addStretch(1)

        self.setLayout(total_Vlayout)

        self.setWindowTitle('GUI_SYSTEM')
        self.setGeometry(300, 300, 300, 200)
        self.showMaximized()

    def Qlabel_style(self, name):
        label = QLabel(name)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("border-style: solid; "
                                  "border-width: 10px; "
                                  "border-color: #dbd9d9; "
                                  "border-radius:20px;"
                                  "padding:10% 0; "
                                  "background-color: #ffffff")
        font = label.font()
        font.setBold(True)
        font.setPointSize(55)
        label.setFont(font)
        return label

    def total_layout(self):
        layout = QHBoxLayout()
        total_title = self.Qlabel_style('Total')
        self.total_label = self.Qlabel_style('-')
        layout.addWidget(total_title)
        layout.addWidget(self.total_label)
        return layout

    def normal_layout(self):
        layout = QHBoxLayout()
        normal_title = self.Qlabel_style('Normal')
        normal_title.setStyleSheet("border-style: solid;"
                                  "border-width: 10px; "
                                  "border-color: #dbd9d9;"
                                  "border-radius:20px;"
                                  "padding: 10% 0; "
                                  "background-color: #66B2FF")
        self.normal_label = self.Qlabel_style('-')
        layout.addWidget(normal_title)
        layout.addWidget(self.normal_label)
        return layout

    def abnormal_layout(self):
        layout = QHBoxLayout()
        abnormal_title = self.Qlabel_style('Abnormal')
        abnormal_title.setStyleSheet("border-style: solid; "
                                     "border-width: 10px; "
                                     "border-color: #dbd9d9; "
                                    "border-radius:20px;"
                                    "padding:10% 0; "
                                    "background-color: #F24949")
        self.abnormal_label = self.Qlabel_style('-')
        layout.addWidget(abnormal_title)
        layout.addWidget(self.abnormal_label)
        return layout

    def listview_layout(self):
        layout = QVBoxLayout()
        self.listview = QListWidget()
        self.listview.setSpacing(20)
        self.listview.setStyleSheet("border-style: solid; "
                                  "border-width: 4px; "
                                  "border-color: #dbd9d9; "
                                  "border-radius:20px;"
                                  "padding:20%; "
                                  "background-color: #FFFFFF")
        font = self.listview.font()
        font.setPointSize(17)
        self.listview.setFont(font)
        layout.addWidget(self.listview)
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
            for file in self.sched.get_new_file():
                self.listview.addItem(file)
            self.sched.update_dir_list()
        else:
            print("new file is not detected")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()

    # scheduler = QtScheduler()
    # scheduler.add_job(ex.update, 'interval', seconds=20)
    # scheduler.start()

    sys.exit(app.exec_())