#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import GUI_kitech

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def load_layout(self):
        layout = QHBoxLayout()
        
        self.load_label = QLabel('Title:')
        self.load_label.setAlignment(Qt.AlignHCenter)
        self.load_label.setStyleSheet(
            "border-style: solid; border-width: 2px; border-color: #dbd9d9; padding:10% 0;")
        layout.addWidget(self.load_label, 3)
        
        load_btn = QPushButton("load",self)
        load_btn.clicked.connect(self.btn_FileLoad)
        load_btn.setStyleSheet(
            "padding:10% 0;")
        layout.addWidget(load_btn, 1)
    
        return layout
        
    def initUI(self):
        self.tab2 = GUI_kitech.MyApp()
        # self.tab3 = GUI_hanyang.MyApp()
        tabs = QTabWidget()
        tabs.addTab(self.tab2, 'KITECH')
        # tabs.addTab(self.tab3, 'HANYANG')

        vbox = QVBoxLayout()
        vbox.addLayout(self.load_layout())
        vbox.addWidget(tabs)

        self.setLayout(vbox)


        self.setWindowTitle('My First Application')
        self.setWindowIcon(QIcon('./Image/kitech.png'))
        self.show()

    def btn_FileLoad(self):

        fname=QFileDialog.getOpenFileName(self, '', '', 'tdms(*.tdms)')   
        self.load_label.setText(str(fname[0].split("/")[-1]))
        self.tab2.btn_fun_FileLoad(fname[0])
        # self.tab3.btn_fun_FileLoad(fname[0])
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

