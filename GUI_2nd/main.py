import sys
from PyQt5.QtWidgets import QApplication
from apscheduler.schedulers.qt import QtScheduler
from kitech_gui.gui import gui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui_system = gui.GUI()

    scheduler = QtScheduler()
    scheduler.add_job(gui_system.update, 'interval', seconds=20)
    scheduler.start()

    sys.exit(app.exec_())