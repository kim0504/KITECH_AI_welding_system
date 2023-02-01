import tensorflow as tf
import numpy as np

class Model():
    def __init__(self, model_name):
        self._model = tf.keras.models.load_model("".join(['./',model_name]))

    def predict(self, array):
        return self._model.predict(array)

    def total_result(self, predict):
        normal = len(np.where(predict<0.5)[0])
        abnormal = len(predict)-normal
        return len(predict), normal, abnormal