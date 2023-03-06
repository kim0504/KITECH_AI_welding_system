import numpy as np

from kitech_gui.model import model, representation
from kitech_gui.scheduler import directory
from apscheduler.schedulers.background import BackgroundScheduler

class scheduler(BackgroundScheduler):
    def __init__(self):
        super().__init__(timezone='Asia/Seoul')

    def job3(self):
        rep = representation.representation()
        mod = model.Model(model)
        dir = directory.dir_info()

        temp = rep.merge_df(dir.inner_list())
        convert = rep.transform_2D(temp, 9000, 28)
        a = mod.predict(convert)
        normal = len(np.where(a < 0.5)[0])
        print(len(a), normal, len(a) - normal, sep="\n")



