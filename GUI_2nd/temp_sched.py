import time, directory, representation
import model
import numpy as np
from apscheduler.schedulers.background import BackgroundScheduler

class my_sched(BackgroundScheduler):
    def __init__(self):
        super().__init__()
        self.cnt = 0

    @classmethod
    def get_cls(cls):
        return cls.__init__()

    def job2(self):
        print(f'count : {self.cnt}')
        self.cnt += 1
        print(f'job2 : {time.strftime("%H:%M:%S")}')

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

    sched.update((len(a), normal, len(a) - normal))


sched = my_sched()

sched.add_job(job3, 'interval', seconds=5, id='test_1')


print('sched before~')
sched.start()
print('sched after~')

while True:
    time.sleep(1)