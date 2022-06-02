import DataSet
import matplotlib.pyplot as plt
from datetime import datetime
from tensorflow import keras
from keras import regularizers
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPool2D, ZeroPadding2D
from keras.layers.normalization.batch_normalization import BatchNormalization


class Model:
    def __init__(self):
        self.model = Sequential()
        data = DataSet.DataSet()
        self.x_train, self.y_train = data.get_train_date()
        self.history = None
        self.dt_string = None

        # Convolutional / Pooling Layers
        self.model.add(Conv2D(filter=32,
                              kernel_size=(3, 3),
                              input_shape=(32, 32, 3),
                              padding='same',
                              kernel_regularizer=regularizers.l2(1e-4)))

        self.model.add(Activation('relu'))
        self.model.add(BatchNormalization())
        self.model.add(Conv2D(filters=32,
                              kernel_size=(3, 3),
                              padding='same',
                              kernel_regularizer=regularizers.l2(1e-4)))

        self.model.add(Activation('relu'))
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D(pool_size=(2, 2)))
        self.model.add(Dropout(rate=0.3))

        self.model.add(Conv2D(filter=64,
                              kernel_size=(3, 3),
                              padding='same',
                              kernel_regularizer=regularizers.l2(1e-4)))

        self.model.add(Activation('relu'))
        self.model.add(BatchNormalization())
        self.model.add(Conv2D(filters=64,
                              kernel_size=(3, 3),
                              padding='same',
                              kernel_regularizer=regularizers.l2(1e-4)))

        self.model.add(Activation('relu'))
        self.model.add(BatchNormalization())
        self.model.add(MaxPool2D(pool_size=(2, 2)))
        self.model.add(Dropout(rate=0.3))

        # Backpropagation Layers
        self.model.add(Flatten())
        self.model.add(Dropout(rate=0.5))
        self.model.add(Dense(1024, activation='relu'))
        self.model.add(Dropout(rate=0.5))
        self.model.add(Dense(10, activation='softmax'))

    # Detail information of whole Neural Network
    def summary(self):
        print(self.model.summary())

    # Training
    def train(self):

        now = datetime.now()
        self.dt_string = now.strftime("%Y%m%d%H%M")
        opt = keras.optimizers.Adam(learning_rate=0.001)
        self.model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
        self.history = self.model.fit(self.x_train, self.y_train, validation_split=0.2,
                                      epochs=50, batch_size=64, verbose=1)

    # Plotting the training history
    def show_history(self, y_label, train_acc, test_acc):
        plt.plot(self.history.history[train_acc])
        plt.plot(self.history.history[test_acc])
        plt.title('Train History')
        plt.xlabel('Epoch')
        plt.ylabel(y_label)
        plt.legend(['train', 'valid'], loc='upper left')
        plt.savefig('./figure/' + self.dt_string + y_label + '.png')

    # Saving the model
    def save(self):
        self.model.save('./model/' + self.dt_string + '.h5')
