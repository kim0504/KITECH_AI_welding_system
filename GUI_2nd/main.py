import sys
from PyQt5.QtWidgets import QApplication
from apscheduler.schedulers.qt import QtScheduler
import directory
import representation
import model
import gui
import numpy as np


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = gui.GUI()

    scheduler = QtScheduler()
    scheduler.add_job(ex.update, 'interval', seconds=20)
    scheduler.start()

    sys.exit(app.exec_())