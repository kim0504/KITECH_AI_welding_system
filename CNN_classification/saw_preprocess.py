# -*- coding: utf-8 -*-
"""SAW_preprocess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ru_zztDZWf4rXpxD85MuwgkVsB5hYcRZ

##Import
"""

# pip install npTDMS

import os, glob
import zipfile
from nptdms import TdmsFile
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

"""## Preprocessing

###data load

결함 데이터 전처리 과정</br>
zip 형태로 전처리를 진행</br>
정상 데이터와 load 부분이 다름
"""

PATH = '/content/drive/MyDrive/colab/SAW_defects_detection/dataset/'

#abnormal data의 경우 zip 파일을 사용했기 때문에 압축을 풀어주는 과정의 코드

path_to_zip_file = PATH+'defect_data.zip'
defect_directory = '/data/defect'

with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
    zip_ref.extractall(defect_directory)

wet_flux_PATH = defect_directory+'/wet_flux/'
oiled_PATH = defect_directory+'/oiled/'
rust_PATH = defect_directory+'/rust/'

#dataset 경로를 설정해서 사용

def tdms_dict(PATH):

  data_list = sorted(os.listdir(PATH))
  df_dic = {}

  for file in data_list:
    tdms_file = TdmsFile(PATH + file)
    tdms_df = tdms_file["Untitled"].as_dataframe()
    df_dic[file] = tdms_df
    
  return df_dic

# normal_dict = tdms_dict(normal_PATH)
rust_dict = tdms_dict(rust_PATH)
oiled_dict = tdms_dict(oiled_PATH)
wet_flux_dict = tdms_dict(wet_flux_PATH)

"""정상 데이터 전처리 과정</br>
결함 데이터와 load 부분이 다름 
"""

DATA_PATH = '/content/drive/MyDrive/colab/SAW_defects_detection/dataset/SAW_data'

#normal, abnormal data를 기록해둔 txt파일을 리스트로 변환
#txt파일의 위치를 설정해서 사용

def txt_to_list(FILE_PATH):

  txt_list = []
  file = open(FILE_PATH, 'r')
  
  while True:
      line = file.readline()
      if not line: break
      txt_list.append(line)

  file.close()

  return txt_list

normal_txt = txt_to_list("/content/drive/MyDrive/colab/용접 파형/normal_list.txt")
abnormal_txt = txt_to_list("/content/drive/MyDrive/colab/용접 파형/abnormal_list.txt")

#미리 사용할 tdms 데이터 리스트를 통해 파일을 dataframe으로 변환

def tdms_to_df(PATH, txt_list):
 
  df_dic = {}

  for file in txt_list:
    try:
      tdms_file = TdmsFile(f'{PATH}/{file[:-1]}.tdms')
      tdms_df = tdms_file["Untitled"].as_dataframe()
      df_dic[file] = tdms_df
    except:
      print("none")
    
  return df_dic

normal_dict = tdms_to_df(DATA_PATH, normal_txt)

"""###processing"""

#데이터에서 용접이 진행되지 않는 부분을 처리
#추후 수정 필요
# no_work_preprocessing(전처리할 dict 형태 데이터, 한 이미지로 만들 시퀀스 크기)

def no_work_preprocessing(tdms_dict, size):

  temp_dict = {}

  for name, data in tdms_dict.items():
    WELD = np.where(data['Voltage']>100)[0]
    print(f'data size : {WELD.shape[0]}',end=' ... ')

    if(WELD.shape[0] > size):
      print("ok")
      temp_dict[name] = data[WELD[0]:WELD[-1]+1].reset_index(drop=True)
    else:
      print("small")
      
  return temp_dict

#하나의 이미지 생성에 사용되는 시퀀스 크기로 전체 데이터를 분할
# array_split(dataframe, 한 이미지로 만들 시퀀스 크기)

def array_split(array, size):

  return [np.array(array.index)[i * size:(i + 1) * size] for i in range((len(array) + size - 1) // size )]

#행렬 변환을 위한 범위 설정
#dataframe의 최댓값,최솟값을 양 끝 범위로 설정

def set_range(tdms_df):
  
  I = tdms_df['Voltage']
  V = tdms_df['Voltage_0']

  I_minmax=[I.min(), I.max()]
  V_minmax=[V.min(), V.max()]

  return I_minmax, V_minmax

#Trainsition matrix 생성

def transition_matrix(I_data, V_data, res):

  transMat_I=np.zeros([res+2,res+2])
  transMat_V=np.zeros([res+2,res+2])

  for j in range(len(I_data)-1):
      if I_data[j+1]>res:
          print(I_data[j+1])
      transMat_I[I_data[j],I_data[j+1]]=transMat_I[I_data[j],I_data[j+1]]+1
      transMat_V[V_data[j],V_data[j+1]]=transMat_V[V_data[j],V_data[j+1]]+1
      
  return transMat_I, transMat_V

#Concurrency matrix 생성

def concurrency_matrix(I_data, V_data, res):
  
  conMat=np.zeros([res+2,res+2])
  for j in range(len(I_data)):
      conMat[I_data[j],V_data[j]]=conMat[I_data[j],V_data[j]]+1
  return conMat

# 하나의 tdms 파일을 이미지로 변환하는 코드
# 변환 후 normalization 진행 

""" 순서
전류,전압 데이터 설정
위 데이터를 설정한 해상도 크기로 분할
각 행렬로 변환
normalization

예를 들어 90000개의 시퀀스를 갖는 데이터를 9000개 간격으로 30x30 해상도를 갖는 이미지로 만들면
(10, 30, 30, 3) 형태를 가짐
"""

def generate_matirces(tdms_df, res):
  
  arr_I = np.array(tdms_df['Voltage'])
  arr_V = np.array(tdms_df['Voltage_0'])

  bins_I=np.arange(I_minmax[0],I_minmax[1],(I_minmax[1]-I_minmax[0])/res )
  bins_V=np.arange(V_minmax[0],V_minmax[1],(V_minmax[1]-V_minmax[0])/res )

  digt_I=np.digitize(arr_I,bins=bins_I)
  digt_V=np.digitize(arr_V,bins=bins_V)

  transMat_I, transMat_V = transition_matrix(digt_I, digt_V, res)
  conMat = concurrency_matrix(digt_I, digt_V, res)

  scaler=MinMaxScaler()
  scaled_conMat=scaler.fit_transform(conMat) # 0~1사이로 정규화
  scaled_transMat_I=scaler.fit_transform(transMat_I)
  scaled_transMat_V=scaler.fit_transform(transMat_V)
  con_trans=np.stack([scaled_transMat_I,scaled_transMat_V,scaled_conMat],axis=2)

  return con_trans

# 특정 클래스에 있는 모든 파일들을 이미지 형태로 변환 
# transform_2D(tdms_dict, 한 이미지로 만들 시퀀스 크기, 해상도 크기-2)

def transform_2D(tdms_dict, size, res):
  
  temp_list = []
  tdms_dict = no_work_preprocessing(tdms_dict, size)

  for _,tdms_df in tdms_dict.items():
    if len(tdms_df) > size:
      global I_minmax, V_minmax
      I_minmax, V_minmax = set_range(tdms_df)
      split_index = array_split(tdms_df, size)

      for index in split_index:
        con_trans = generate_matirces(tdms_df[index[0]:index[-1]], res)
        temp_list.append(con_trans)
        
  return np.array(temp_list)

"""### 전처리 실행"""

normal_np = transform_2D(normal_dict, 9000, 28)

rust_np_array = transform_2D(rust_dict, 9000, 28)

oiled_np_array = transform_2D(oiled_dict, 9000, 28)

wet_np_array = transform_2D(wet_flux_dict, 9000, 28)

normal_np.shape, rust_np_array.shape, oiled_np_array.shape, wet_np_array.shape

"""##Save"""

np.save("normal_9000_30",normal_np)
np.save("rust_9000_30",rust_np_array)
np.save("oiled_9000_30",oiled_np_array)
np.save("wet_9000_30",wet_np_array)