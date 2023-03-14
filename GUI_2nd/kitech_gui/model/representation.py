"""
용접 전류,전압 파형 2D array로 변환
"""

import pandas as pd
import numpy as np
from nptdms import TdmsFile
from sklearn.preprocessing import MinMaxScaler
from collections import namedtuple
class representation():
    def __init__(self, dir_path:str):
        self.DIR_PATH = dir_path

    """ 컬럼 개수 확인 및 컬럼명 변경, (컬럼명이 통일되지 않았음) """
    def check_columns(self, tdms_df:pd.DataFrame)->pd.DataFrame:
        if len(tdms_df.columns) == 5:
            tdms_df.columns = ['Time', 'Voltage', 'Voltage_0', 'Voltage_1', 'Rotation_angle']
        elif len(tdms_df.columns) == 4:
            tdms_df.columns = ['Time', 'Voltage', 'Voltage_0', 'Voltage_1']
        return tdms_df

    """ tdms 파일을 DataFrame으로 변환 """
    def tdms_to_df(self, file_name:TdmsFile)->pd.DataFrame:
        tdms_file = TdmsFile("".join([self.DIR_PATH,file_name]))
        tdms_df = tdms_file["Untitled"].as_dataframe()
        tdms_df = self.check_columns(tdms_df)
        return tdms_df

    """ 파일이 여러 개 들어온 경우, 병합해서 하나의 값으로 반환 """
    def merge_df(self, files:list)->pd.DataFrame:
        df_list = []
        for file in files:
            df_list.append(self.tdms_to_df(file))
        if len(df_list)>1:
            return pd.concat(df_list)
        elif len(df_list)==1:
            return df_list[0]
        #들어온 값이 한개도 없을 때 처리 코드 필요

    """ 이상치 제거를 위한 범위 클리핑
        상위,하위 0.0001% 값으로 제한 """
    def set_range(self, tdms_df:pd.DataFrame)->tuple:
        range = namedtuple('Range', ['min', 'max'])

        I_range = range(tdms_df['Voltage'].quantile(q=0.0001, interpolation='nearest'),
                    tdms_df['Voltage'].quantile(q=0.9999, interpolation='nearest'))
        V_range = range(tdms_df['Voltage_0'].quantile(q=0.0001, interpolation='nearest'),
                    tdms_df['Voltage_0'].quantile(q=0.9999, interpolation='nearest'))
        return I_range, V_range

    """ MTF를 사용한 matrix 변환. res의 크기를 갖는 해상도로 변환 """
    def transition_matrix(self, I_data:tuple, V_data:tuple, res:int)->tuple:
        transMat_I=np.zeros([res+2,res+2])
        transMat_V=np.zeros([res+2,res+2])
        for j in range(len(I_data)-1):
            transMat_I[I_data[j],I_data[j+1]] += 1
            transMat_V[V_data[j],V_data[j+1]] += 1
        return transMat_I, transMat_V

    """ I-V curve를 사용한 matrix 변환. res의 크기를 갖는 해상도로 변환 """
    def concurrency_matrix(self, I_data:tuple, V_data:tuple, res:int)->np.array:
        conMat=np.zeros([res+2,res+2])
        for j in range(len(I_data)):
            conMat[I_data[j],V_data[j]] += 1
        return conMat

    """ 하나의 부분에 대해 2D로 변환 후 3개 matrix 병합 및 스케일링 """
    def generate_matirces(self, tdms_df:pd.DataFrame, res:int)->np.array:
        arr_I = np.array(tdms_df['Voltage'])
        arr_V = np.array(tdms_df['Voltage_0'])

        bins_I=np.arange(I_range.min,I_range.max,(I_range.max-I_range.min)/res)
        bins_V=np.arange(V_range.min,V_range.max,(V_range.max-V_range.min)/res)

        digt_I=np.digitize(arr_I,bins=bins_I)
        digt_V=np.digitize(arr_V,bins=bins_V)

        transMat_I, transMat_V = self.transition_matrix(digt_I, digt_V, res)
        conMat = self.concurrency_matrix(digt_I, digt_V, res)

        scaler=MinMaxScaler()
        scaled_conMat=scaler.fit_transform(conMat) # 0~1사이로 정규화
        scaled_transMat_I=scaler.fit_transform(transMat_I)
        scaled_transMat_V=scaler.fit_transform(transMat_V)
        con_trans=np.stack([scaled_transMat_I,scaled_transMat_V,scaled_conMat],axis=2)

        return con_trans

    """ 파일 전체를 size 크기로 분할 후 res의 해상도를 갖는 2D array로 변환 """
    def transform_2D(self, tdms_df:pd.DataFrame, size:int, res:int)->np.array:
        temp_list = []
        try:
            if len(tdms_df) > size:
                global I_range, V_range
                I_range, V_range = self.set_range(tdms_df)
                for i in range(0, len(tdms_df), size):
                    con_trans = self.generate_matirces(tdms_df[i:i+size], res)
                    temp_list.append(con_trans)
        except:
            return None
        return np.array(temp_list)
