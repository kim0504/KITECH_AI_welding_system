import numpy as np

from kitech_gui.model import model, representation
from kitech_gui.scheduler import directory
from apscheduler.schedulers.background import BackgroundScheduler
import tensorflow as tf

class scheduler(BackgroundScheduler):
    def __init__(self):
        super().__init__(timezone='Asia/Seoul')

    def job3(self):
        rep = representation.representation()
        mod = model.Model(model_path)
        dir = directory.dir_info(file_path)

        temp = rep.merge_df(dir.inner_list())
        convert = rep.transform_2D(temp, 9000, 28)
        a = mod.predict(convert)
        normal = len(np.where(a < 0.5)[0])
        print(len(a), normal, len(a) - normal, sep="\n")

if __name__ == '__main__':
    pass
    model_path = "E:\welding_defect_detection_binary\Model\kitech_binary.h5"  # 수정 필요
    file_path = "../GUI_2nd_temp"
    sched = directory.dir_info(file_path)
    preprocess = representation.representation()
    temp = preprocess.merge_df(sched.inner_list())
    convert = preprocess.transform_2D(temp, 9000, 28)
    print(convert.shape)
    model = tf.keras.models.load_model(model_path)
    a = model.predict(convert)
    normal = len(np.where(a<0.5)[0])
    print(len(a),normal,len(a)-normal, sep="\n")



