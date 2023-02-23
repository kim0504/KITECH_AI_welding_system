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

    def create_result_txt(self, total:int, normal:int):
        result_path = './result'
        if 'result' not in os.listdir():
            os.mkdir("./result")
        with open('/'.join([result_path, ".".join([str(self.get_new_file()),'txt'])]), 'w') as f:
            f.write(f'{" ".join([str(total),str(normal),str(total-normal)])}')
            f.close()