from nptdms import TdmsFile
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

class representation():
    def __init__(self):
        self.DIR_PATH = '../'

    def tdms_to_df(self, file_name:TdmsFile)->pd.DataFrame:
        tdms_file = TdmsFile("".join([self.DIR_PATH,file_name]))
        tdms_df = tdms_file["Untitled"].as_dataframe()
        if len(tdms_df.columns) == 5:
            tdms_df.columns = ['Time', 'Voltage', 'Voltage_0', 'Voltage_1', 'Rotation_angle']
        elif len(tdms_df.columns) == 4:
            tdms_df.columns = ['Time', 'Voltage', 'Voltage_0', 'Voltage_1']
        return tdms_df

    def merge_df(self, files:list)->pd.DataFrame:
        df_list = []
        for file in files:
            df_list.append(self.tdms_to_df(file))
        if len(df_list)>1:
            return pd.concat(df_list)
        elif len(df_list)==1:
            return df_list[0]

    def set_range(self, tdms_df):
        I_minmax = [tdms_df['Voltage'].quantile(q=0.0001, interpolation='nearest'),
                    tdms_df['Voltage'].quantile(q=0.9999, interpolation='nearest')]
        V_minmax = [tdms_df['Voltage_0'].quantile(q=0.0001, interpolation='nearest'),
                    tdms_df['Voltage_0'].quantile(q=0.9999, interpolation='nearest')]
        return I_minmax, V_minmax

    def transition_matrix(self, I_data, V_data, res):
        transMat_I=np.zeros([res+2,res+2])
        transMat_V=np.zeros([res+2,res+2])
        for j in range(len(I_data)-1):
            transMat_I[I_data[j],I_data[j+1]] += 1
            transMat_V[V_data[j],V_data[j+1]] += 1
        return transMat_I, transMat_V

    def concurrency_matrix(self, I_data, V_data, res):
        conMat=np.zeros([res+2,res+2])
        for j in range(len(I_data)):
            conMat[I_data[j],V_data[j]] += 1
        return conMat

    def generate_matirces(self, tdms_df, res):
        arr_I = np.array(tdms_df['Voltage'])
        arr_V = np.array(tdms_df['Voltage_0'])

        bins_I=np.arange(I_minmax[0],I_minmax[1],(I_minmax[1]-I_minmax[0])/res)
        bins_V=np.arange(V_minmax[0],V_minmax[1],(V_minmax[1]-V_minmax[0])/res)

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

    def transform_2D(self, tdms_df, size, res):
        temp_list = []
        try:
            if len(tdms_df) > size:
                global I_minmax, V_minmax
                I_minmax, V_minmax = self.set_range(tdms_df)
                for i in range(0, len(tdms_df), size):
                    con_trans = self.generate_matirces(tdms_df[i:i+size], 28)
                    temp_list.append(con_trans)

        except:
            return None

        return np.array(temp_list)
