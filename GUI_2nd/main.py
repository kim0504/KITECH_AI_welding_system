import sys
from PyQt5.QtWidgets import QApplication

from kitech_gui.gui import gui
from kitech_gui.scheduler import scheduler

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui_system = gui.GUI()

    scheduler = scheduler.WeldingScheduler(gui_system)
    scheduler.add_job(scheduler.update, 'interval', seconds=60)
    scheduler.start()

    sys.exit(app.exec_())