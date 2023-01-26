from datetime import datetime


def qt_schedule():
    import signal
    import sys
    from apscheduler.schedulers.qt import QtScheduler

    try:
        from PyQt5.QtWidgets import QApplication, QLabel
    except ImportError:
        from PyQt5.QtGui import QApplication, QLabel


    def tick():
        label.setText('Tick! The time is: %s' % datetime.now())

    app = QApplication(sys.argv)

    # This enables processing of Ctrl+C keypresses
    signal.signal(signal.SIGINT, lambda *args: QApplication.quit())

    label = QLabel('The timer text will appear here in a moment!')
    label.setWindowTitle('QtScheduler example')
    label.setFixedSize(480, 100)
    label.show()

    scheduler = QtScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    scheduler.start()

    # Execution will block here until the user closes the windows or Ctrl+C is pressed.
    app.exec_()

qt_schedule()