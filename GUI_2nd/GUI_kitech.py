import sys
import kitech_preprocess as saw
import custom_listwidget as ListWidget

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

global model
model = tf.keras.models.load_model('./Model/kitech_binary.h5')

class MyApp(QWidget):
    
    def __init__(self):
        super().__init__()
        self.i = -1
        self.np_array = np.array([])
        self.pred = []
        self.label = []
        self.data_dict = {'0':'Normal', '1':'wet flux', '2':'oiled', '3':'rust', '4':'no welding'}
        self.initUI()

    def label_layout(self):
        layout = QHBoxLayout()
        
        self.label_label = QLabel('Predict lable')
        self.label_label.setFixedHeight(60);   
        self.label_label.setAlignment(Qt.AlignCenter)        
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
        
        right_layout = QVBoxLayout()
        
        pixmap1 = QPixmap("./Image/grey.png").scaled(120,120)
        pixmap2 = QPixmap("./Image/grey.png").scaled(120,120)
        pixmap3 = QPixmap("./Image/grey.png").scaled(120,120)

        self.lbl_img1 = QLabel()
        self.lbl_img1.setAlignment(Qt.AlignHCenter)
        self.lbl_img1.setPixmap(pixmap1)
        
        self.lbl_img2 = QLabel()
        self.lbl_img2.setAlignment(Qt.AlignHCenter)
        self.lbl_img2.setPixmap(pixmap2)
        
        self.lbl_img3 = QLabel()
        self.lbl_img3.setAlignment(Qt.AlignHCenter)
        self.lbl_img3.setPixmap(pixmap3)

        right_layout.addWidget(self.lbl_img1)
        right_layout.addWidget(self.lbl_img2)
        right_layout.addWidget(self.lbl_img3)
        
        layout = QHBoxLayout()
        layout.addLayout(left_layout,3)
        layout.addLayout(right_layout,1)
        
        return layout
        
    def Clicked(self,item):
        self.i = int(self.listWidget.currentRow())
        print(self.listWidget.currentItem().text())
        self.label6.setText(str(round(1-self.pred[self.i][0],3)))
        self.label7.setText(str(round(self.pred[self.i][0],3)))
        self.print_matrix()
        if self.label[self.i] == 0:
            self.label_label.setText(f'Normal weld')
        else:
            self.label_label.setText(f'Abnormal')
        
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
        
        self.label1.setFixedHeight(50)
        self.label2.setFixedHeight(50)
        self.label6.setFixedHeight(50)
        self.label7.setFixedHeight(50)
        
        result_value_style = "border-style: solid; border-width: 2px; border-color: #dbd9d9; background-color: #ffffff"  
        
        self.label6.setStyleSheet(result_value_style)
        self.label7.setStyleSheet(result_value_style)
        
        grid.addWidget(self.label1, 0, 0)
        grid.addWidget(self.label2, 0, 1)
        grid.addWidget(self.label6, 1, 0)
        grid.addWidget(self.label7, 1, 1)
        
        return grid

    
    def initUI(self):
        
        total_layout = QVBoxLayout()
        total_layout.addLayout(self.visual_layout())
        total_layout.addLayout(self.label_layout())
        total_layout.addLayout(self.result_layout())
        
        self.setLayout(total_layout)
        
        self.setWindowTitle('My First Application')
        self.setWindowIcon(QIcon('./Image/kitech.png'))
        self.setFixedSize(QSize(600, 700))
#         self.move(300, 300)
#         self.resize(400, 200)   

        
    def btn_fun_FileLoad(self, files):
        self.listWidget.clear()
        tdms = saw.merge_df(files)
        convert_tdms = saw.transform_2D(tdms, 9000, 28)
        self.np_array = convert_tdms
        self.pred = model.predict(convert_tdms)
        self.label = np.where(model.predict(convert_tdms)>0.5,1,0)
        
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


    def print_matrix(self):
        plt.imsave("./Image/temp_image/I_transition.png", self.np_array[self.i,:,:,0])
        plt.imsave("./Image/temp_image/V_transition.png", self.np_array[self.i,:,:,1])
        plt.imsave("./Image/temp_image/Co_occurrence.png", self.np_array[self.i,:,:,2])
        
        pixmap1 = QPixmap("./Image/temp_image/I_transition.png").scaled(120,120)
        pixmap2 = QPixmap("./Image/temp_image/V_transition.png").scaled(120,120)
        pixmap3 = QPixmap("./Image/temp_image/Co_occurrence.png").scaled(120,120)
        
        self.lbl_img1.setPixmap(pixmap1)
        self.lbl_img2.setPixmap(pixmap2)
        self.lbl_img3.setPixmap(pixmap3)
        
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    app.exec_()