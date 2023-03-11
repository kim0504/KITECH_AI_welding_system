import os

class Directory():
    def __init__(self):
        self._file_path = '../'
        self._file_list = self.get_only_tdms()

    def dir_list(self):
        print(self.get_only_tdms())

    def used_list(self):
        print(self._file_list)
        return self._file_list

    def update_list(self):
        self._file_list = self.get_only_tdms()
        print("dir update")
        print(self._file_list)

    def search_new_file(self):
        print("current : ", self.get_only_tdms())
        print("past : ", self._file_list)
        return list(set(self.get_only_tdms()) - set(self._file_list))

    def get_only_tdms(self):
        return [file for file in os.listdir(self._file_path) if file.endswith(".tdms")]

    def create_result_txt(self, total:int, normal:int):
        result_path = '../result'
        if 'result' not in os.listdir('../'):
            os.mkdir("../result")
        with open('/'.join([result_path, ".".join([str(self.search_new_file()),'txt'])]), 'w') as f:
            f.write(f'{" ".join([str(total),str(normal),str(total-normal)])}')
            f.close()
        return 0