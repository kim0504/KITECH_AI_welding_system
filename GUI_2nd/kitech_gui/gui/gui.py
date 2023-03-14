"""
GUI 코드
전체 예측 개수, 정상 예측 개수, 비정상 예측 개수를 표시하는 레이아웃과
현재까지 예측에 사용된 파일들의 이름을 표시하는 리스트뷰 레이아웃으로 구성
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidget
from PyQt5.QtCore import Qt
from kitech_gui.scheduler import directory
from kitech_gui.model import representation

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self._total = 0
        self._normal = 0
        self._abnormal = 0
        self.sched = directory.Directory()
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
        total_title.setStyleSheet("border-style: solid;"
                                  "border-width: 10px; "
                                  "border-color: #dbd9d9;"
                                  "border-radius:20px;"
                                  "padding: 10% 0; "
                                  "background-color: #dbd9d9")
        layout.addWidget(total_title)
        layout.addWidget(self.total_label)
        return layout

    def normal_layout(self):
        layout = QHBoxLayout()
        normal_title = self.Qlabel_style('Normal')
        normal_title.setStyleSheet("color:#FFFFFF;"
                                   "border-style: solid;"
                                  "border-width: 10px; "
                                  "border-color: #0080FF;"
                                  "border-radius:20px;"
                                  "padding: 10% 0; "
                                  "background-color: #0080FF")
        self.normal_label = self.Qlabel_style('-')
        layout.addWidget(normal_title)
        layout.addWidget(self.normal_label)
        return layout

    def abnormal_layout(self):
        layout = QHBoxLayout()
        abnormal_title = self.Qlabel_style('Abnormal')
        abnormal_title.setStyleSheet("color:#FFFFFF;"
                                     "border-style: solid; "
                                     "border-width: 10px; "
                                     "border-color: #F03434; "
                                    "border-radius:20px;"
                                    "padding:10% 0; "
                                    "background-color: #F03434")
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