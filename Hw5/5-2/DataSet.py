import numpy as np
from keras.utils import np_utils
from keras.datasets import cifar10
np.random.seed(10)


class DataSet:
    def __init__(self):

        # loading the data
        (self.x_train, self.y_train), (self.x_test, self.y_test) = cifar10.load_data()
        print("test data -> images: {} / labels: {}".format(self.x_test.shape, self.y_test.shape))

        # normalize / onehot encoding
        self.x_train_normalize = self.x_train.astype('float32') / 255.0
        self.x_test_normalize = self.x_test.astype('flloat32') / 255.0
        self.y_train_onehot = np_utils.to_categorical(self.y_train)
        self.y_test_onehot = np_utils.to_categorical(self.y_test)

    def get_train_date(self):
        print("original train data -> images: {} / labels: {}".format(self.x_train.shape, self.y_train.shape))
        print("processed train data -> images: {} / labels: {}".
              format(self.x_train_normalize.shape, self.y_train_onehot.shape))
        return self.x_train_normalize, self.y_train_onehot
