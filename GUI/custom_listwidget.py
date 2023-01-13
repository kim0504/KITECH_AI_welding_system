import sys
#from PyQt4 import QtGui
from PyQt5 import QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import *
from PyQt5.QtCore import QSize

class QCustomQWidget(QWidget):                       # QtWidgets
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.icon_label = QtWidgets.QLabel() 
        self.num_label = QtWidgets.QLabel()               # QtWidgets
        self.state_label = QtWidgets.QLabel()               # QtWidgets
        self.angle_label = QtWidgets.QLabel()
        
        self.num_label.setAlignment(Qt.AlignCenter)
        self.state_label.setAlignment(Qt.AlignCenter)
        self.angle_label.setAlignment(Qt.AlignCenter)
        
        self.allQHBoxLayout  = QtWidgets.QHBoxLayout()          # QtWidgets
        self.allQHBoxLayout.addWidget(self.icon_label, 1)
        self.allQHBoxLayout.addWidget(self.num_label, 1)
        self.allQHBoxLayout.addWidget(self.angle_label, 3)
        self.allQHBoxLayout.addWidget(self.state_label, 3)       
        self.setLayout(self.allQHBoxLayout)      

    def add_item(self, icon_path, num, state, angle):
        self.icon_label.setPixmap(QtGui.QPixmap(icon_path).scaled(25, 25))
        self.num_label.setText(num)
        self.state_label.setText(state)
        self.angle_label.setText(angle)