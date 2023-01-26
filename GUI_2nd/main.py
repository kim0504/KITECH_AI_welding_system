import time
from apscheduler.schedulers.background import BackgroundScheduler
import directory
import representation
import scheduler, temp_sched
import gui
import model
import sys
from PyQt5.QtWidgets import QApplication
import numpy as np


def job3():
    model_path = "E:\welding_defect_detection_binary\Model\kitech_binary.h5"  # 수정 필요
    file_path = "../GUI_2nd_temp"
    sched = directory.dir_info(file_path)
    preprocess = representation.representation()
    temp = preprocess.merge_df(sched.inner_list())
    convert = preprocess.transform_2D(temp, 9000, 28)
    print(convert.shape)
    mode = model.Model(model_path)
    a = mode.predict(convert)
    normal = len(np.where(a < 0.5)[0])
    print(len(a), normal, len(a) - normal, sep="\n")

    ex.update((len(a), normal, len(a) - normal))

if __name__ == '__main__':
    # sched = scheduler.scheduler()
    # sched.add_job(sched.job3, 'cron', second='0', id="aaa")
    # sched.start()
    # while (1):
    #     time.sleep(1)

    app = QApplication(sys.argv)

    model_path = "E:\welding_defect_detection_binary\Model\kitech_binary.h5"  # 수정 필요
    file_path = "../GUI_2nd_temp"
    sched = directory.dir_info(file_path)
    preprocess = representation.representation()
    temp = preprocess.merge_df(sched.inner_list())
    convert = preprocess.transform_2D(temp, 9000, 28)
    print(convert.shape)
    mode = model.Model(model_path)
    a = mode.predict(convert)
    normal = len(np.where(a < 0.5)[0])
    print(len(a), normal, len(a) - normal, sep="\n")

    ex = gui.GUI()
    ex.update((len(a), normal, len(a)-normal))

    sys.exit(app.exec_())


