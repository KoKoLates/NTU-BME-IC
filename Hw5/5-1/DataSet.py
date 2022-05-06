from keras.datasets import mnist
from keras.utils import np_utils
import numpy as np
np.random.seed(10)


class DataSet:
    def __init__(self):
        (x_Train, y_Train), (self.x_Test, self.y_Test) = mnist.load_data()
        x_train_4d = x_Train.reshape(x_Train.shape[0], 28, 28, 1).astype('float32')
        x_test_4d = self.x_Test.reshape(self.x_Test.shape[0], 28, 28, 1).astype('float32')
        self.x_Train_4D_normalize = x_train_4d / 255
        self.x_Test_4D_normalize = x_test_4d / 255
        self.y_Train_OneHot = np_utils.to_categorical(y_Train)
        self.y_Test_OneHot = np_utils.to_categorical(self.y_Test)

    def train_data(self):
        return self.x_Train_4D_normalize, self.y_Train_OneHot

    def test_date(self):
        return (self.x_Test, self.y_Test), (self.x_Test_4D_normalize, self.y_Test_OneHot)


data = DataSet()
x_train, y_train = data.train_data()
(x_test, y_test), (x_test_processed, y_test_processed) = data.test_date()

