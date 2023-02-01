import os
from kitech_gui.model import representation


class dir_info():
    def __init__(self, file_path):
        self._file_path = file_path
        self._file_list = os.listdir(self._file_path)

    def dir_list(self):
        print(os.listdir(self._file_path))

    def inner_list(self):
        print(self._file_list)
        return self._file_list

    def update_dir_list(self):
        self._file_list = os.listdir(self._file_path)
        print("dir update")
        print(self._file_list)

    def get_new_file(self):
        print("current : ", os.listdir(self._file_path))
        print("past : ", self._file_list)
        return list(set(os.listdir(self._file_path)) - set(self._file_list))

if __name__ == '__main__':
    a = dir_info("../GUI_2nd_temp")
    a.dir_list()

    preprocess = representation.representation()
    convert = preprocess.transform_2D(preprocess.merge_df(a.inner_list()), 9000, 28)
    print(convert is not None)


