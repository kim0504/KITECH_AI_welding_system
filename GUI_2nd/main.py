import sys
from PyQt5.QtWidgets import QApplication
from apscheduler.schedulers.qt import QtScheduler
import directory
import representation
import model
import gui
import numpy as np

def update():
    global ex
    convert = representation.representation.transform_2D(representation.representation.merge_df(directory.dir_info.get_new_file()), 9000, 28)
    if convert is not None:
        pred = model.Model('kitech_binary.h5').predict(convert)
        normal = len(np.where(pred < 0.5)[0])
        gui._total += len(pred)
        gui._normal += normal
        gui._abnormal += len(pred) - normal
        gui.total_label.setText(str(gui._total))
        gui.normal_label.setText(str(gui._normal))
        gui.abnormal_label.setText(str(gui._abnormal))
    else:
        print("new file is not detected")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = gui.GUI()

    scheduler = QtScheduler()
    scheduler.add_job(ex.update, 'interval', seconds=20)
    scheduler.start()

    sys.exit(app.exec_())