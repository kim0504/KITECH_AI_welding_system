"""
지정한 디렉토리에서 tdms 파일 관련 조회 기능을 수행
새로운 tdms 파일을 탐색하거나 해당 디렉토리에 존재하는 tdms 파일에 대해서 조회
"""

import os

class Directory():
    def __init__(self, dir_path:str):
        self._file_path = dir_path
        self._file_list = self.get_only_tdms() #사용된 파일을 표시하기 위한 리스트

    """ 디렉토리에서 tdms 파일만 출력 """
    def dir_list(self):
        print(self.get_only_tdms())

    """ 사용된 tdms 파일 출력 """
    def used_list(self):
        print(self._file_list)
        return self._file_list

    """ 현재 디렉토리 정보로 리스트 업데이트 """
    def update_list(self):
        self._file_list = self.get_only_tdms()
        print("dir update")
        print(self._file_list)

    """ 새로운 파일 탐색. 현재 디렉토리의 파일 중 file_list에 없는 파일들 반환 """
    def search_new_file(self):
        print("current : ", self.get_only_tdms())
        print("past : ", self._file_list)
        return list(set(self.get_only_tdms()) - set(self._file_list))

    """ 파일 중 tdms 포맷 파일만 반환 """
    def get_only_tdms(self):
        return [file for file in os.listdir(self._file_path) if file.endswith(".tdms")]

    """ 디렉토리에 txt 파일 생성 """
    def create_result_txt(self, total:int, normal:int):
        result_path = '../result'
        if 'result' not in os.listdir('../'):
            os.mkdir("../result")
        with open('/'.join([result_path, ".".join([str(self.search_new_file()),'txt'])]), 'w') as f:
            f.write(f'{" ".join([str(total),str(normal),str(total-normal)])}')
            f.close()
        return 0