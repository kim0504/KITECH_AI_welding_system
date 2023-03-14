import tensorflow as tf
import numpy as np

class Model():
    def __init__(self, model_name):
        self._model = tf.keras.models.load_model("".join(['./',model_name]))

    def predict(self, array):
        return self._model.predict(array)

    """ theshold 값을 0.5로 설정하여 결함 판단 
        전체 개수, 정상 개수, 비정상 개수로 반환"""
    def total_result(self, predict):
        normal = len(np.where(predict<0.5)[0])
        abnormal = len(predict)-normal
        return len(predict), normal, abnormal