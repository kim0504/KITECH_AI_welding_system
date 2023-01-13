#!/usr/bin/env python
# coding: utf-8

import os, glob
# import zipfile
from nptdms import TdmsFile
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import skew, kurtosis

import time
import scipy as sp
import sklearn
from sktime.datatypes._panel._convert import (
    from_3d_numpy_to_nested,
    from_multi_index_to_3d_numpy,
    from_nested_to_3d_numpy,
)

import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler



def tdms_to_df(files):

    df_dic = {}
    
    for file in files:
        try:
            tdms_file = TdmsFile(file)
            tdms_df = tdms_file["Untitled"].as_dataframe()
            df_dic[file] = tdms_df
        except:
            print("none")
    
    return df_dic

def tdms_df(file):
    
    tdms_file = TdmsFile(file)
    tdms_df = tdms_file["Untitled"].as_dataframe()

    return tdms_df

def merge_df(files):
    df_list = []
    for file in files:
        df_list.append(tdms_df(file))
    if len(df_list)>1:
        return pd.concat(df_list)
    elif len(df_list)==1:
        return df_list[0]

def set_range(tdms_df):
  
    I = tdms_df['Voltage']
    V = tdms_df['Voltage_0']

    I_minmax=[I.min(), I.max()]
    V_minmax=[V.min(), V.max()]

    return I_minmax, V_minmax



def array_split(array, size):

    return [np.array(array.index)[i * size:(i + 1) * size] for i in range((len(array) + size - 1) // size )]



def transform_2D(tdms_df, size):
  
    feature_append = np.zeros((1,15))
    tdms_df = tdms_df.drop(['Time', 'Rotation_Angle'], axis = 1)
    global I_minmax, V_minmax
    I_minmax, V_minmax = set_range(tdms_df)
    initial_index = array_split(tdms_df, size)
    split_index = initial_index[0:len(initial_index)//10*10]

    mean = []
    rms = []
    std = []
    kurto = []
    skewness = []

    for index in split_index:
        x = tdms_df[index[0]:index[-1]]

        xm = np.mean(x)
        xrms = np.sqrt(np.mean(x**2))
        xstd = np.std(x)
        xkurto = kurtosis(x)
        xskew = skew(x)

        mean.append(xm)
        a = np.array(mean)
        rms.append(xrms)
        b = np.array(rms)
        std.append(xstd)
        c = np.array(std)
        kurto.append(xkurto)
        d = np.array(kurto)
        skewness.append(xskew)
        e = np.array(skewness)

        f = np.concatenate((a, b, c, d, e), axis=1)
        feature_append = np.concatenate((feature_append, f), axis=0)
    feature_append = np.delete(feature_append, 0, axis=0)

    return feature_append



# 10초씩 데이터 분할
def split_10s(array, step):
    scaler = RobustScaler() # 각 갭별 유효 윈도우 stack 정규화
    scaler.fit(array) # 각 갭별 유효 윈도우 stack 정규화
    array = scaler.transform(array)
    print("scale finish")
    s = []
    for j in range(int(len(array[:,0])/step)):
        s.append(array[j*step:(j+1)*step])
        feature_1s = np.reshape(s,(-1,15,10))
        feature_1s = from_3d_numpy_to_nested(feature_1s)
    return feature_1s



def preprocessing(files):
    data = split_10s(transform_2D(merge_df(files), 1000),10)
    return from_nested_to_3d_numpy(data)