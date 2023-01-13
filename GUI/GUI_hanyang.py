import sys, os
import hanyang_preprocess as preprocess
import custom_listwidget as ListWidget

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

PATH = os.getcwd()
global model
model = tf.keras.models.load_model('./Model/hanyang_lstm.h5')

class MyApp(QWidget):
   
    
    def __init__(self):
        super().__init__()
        self.i = -1
        self.np_array = np.array([])
        self.pred = []
        self.label = []
        self.data_dict = {'0':'Normal', '1':'wet flux', '2':'oiled', '3':'rust'}
        self.initUI()

    def label_layout(self):
        layout = QHBoxLayout()
        
        self.label_label = QLabel('Predict lable')
        self.label_label.setAlignment(Qt.AlignCenter)
        self.label_label.setFixedHeight(70);   
        self.label_label.setStyleSheet(
            "border-style: solid; border-width: 2px; border-color: #dbd9d9; padding:10% 0; background-color: #ffffff")
        font = self.label_label.font()
        font.setPointSize(13)
        self.label_label.setFont(font)
        layout.addWidget(self.label_label)
        return layout
        
        
    def visual_layout(self):
        
        left_layout = QHBoxLayout()        
        
        self.listWidget = QListWidget()
        self.listWidget.setFixedHeight(385)        
        self.listWidget.itemClicked.connect(self.Clicked) # connect itemClicked to Clicked method      
        left_layout.addWidget(self.listWidget)        
        
        layout = QHBoxLayout()
        layout.addLayout(left_layout,3)
        
        return layout
        
    def Clicked(self,item):
        self.i = int(self.listWidget.currentRow())
        print(self.listWidget.currentItem().text())
        self.label6.setText(str(round((self.pred)[self.i][0],3)))
        self.label7.setText(str(round((self.pred)[self.i][1],3)))
#         self.label8.setText(str(round((self.pred)[self.i][2],3)))
#         self.label9.setText(str(round((self.pred)[self.i][3],3)))
        if self.label[self.i] == 0:
            self.label_label.setText(f'Normal')
        elif self.label[self.i] == 4:
            self.label_label.setText(f'No weld')
        else:
            self.label_label.setText(f'{self.data_dict[str(self.label[self.i])]} detected')
        
    def result_layout(self):
        grid = QGridLayout()       
        
        self.label1 = QLabel('Normal')
        self.label2 = QLabel('Abnormal')
        self.label6 = QLabel('-')
        self.label7 = QLabel('-')
        
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label6.setAlignment(Qt.AlignCenter)
        self.label7.setAlignment(Qt.AlignCenter)
        
        st = "border-width: 2px; border-height: 12px;"
        stylesheet = "border-style: solid; border-width: 2px; border-height: 12px; border-color: #dbd9d9; background-color: #ffffff"
        
        self.label1.setStyleSheet(st)
        self.label2.setStyleSheet(st)
        self.label6.setStyleSheet(stylesheet)
        self.label7.setStyleSheet(stylesheet)
        
        grid.addWidget(self.label1, 0, 0)
        grid.addWidget(self.label2, 0, 1)
        grid.addWidget(self.label6, 1, 0)
        grid.addWidget(self.label7, 1, 1)
        
        self.label1.setFixedHeight(50)
        self.label2.setFixedHeight(50)
        self.label6.setFixedHeight(50)
        self.label7.setFixedHeight(50)
        
        return grid

    
    def initUI(self):
        
        total_layout = QVBoxLayout()
        total_layout.addLayout(self.visual_layout(), stretch=4)
        total_layout.addLayout(self.label_layout(), stretch=1)
        total_layout.addLayout(self.result_layout(), stretch=1)
        
        self.setLayout(total_layout)
        
        self.setWindowTitle('My First Application')
        self.setWindowIcon(QIcon(PATH+'/Image/kitech.png'))
        self.setFixedSize(QSize(600, 700))
        self.move(300, 300)
        self.resize(400, 200)   
        
        
        
    def btn_fun_FileLoad(self, files):
        self.listWidget.clear()
        tdms = preprocess.merge_df(files)
        convert_tdms = preprocess.split_10s(preprocess.transform_2D(tdms, 1000),10)
        self.np_array = convert_tdms
        self.pred = model.predict(convert_tdms)
        self.label = model.predict(convert_tdms).argmax(axis=1)
        print(self.label)
        
        for i in range(len(self.label)):
            print(f'{i} ... {self.label[i]}')
            myQCustomQWidget = ListWidget.QCustomQWidget()
            if self.label[i] == 0:                
                myQCustomQWidget.add_item('./Image/blue.png', f'{str(i+1)} / {len(self.label)}', 'Normal', 
                                          f"{round((tdms[i*9000:(i+1)*9000])['Rotation_Angle'].mean(), 2)}")                
            else:
                myQCustomQWidget.add_item('./Image/red.png', f'{str(i+1)} / {len(self.label)}', 'Abnormal', 
                                          f"{round((tdms[i*9000:(i+1)*9000])['Rotation_Angle'].mean(), 2)}")
            myQListWidgetItem = QListWidgetItem(self.listWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.listWidget.addItem(myQListWidgetItem)
            self.listWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)       
        
        
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    app.exec_()