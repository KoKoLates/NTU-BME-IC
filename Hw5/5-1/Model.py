from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from datetime import datetime
import matplotlib.pyplot as plt


class Model:
    def __init__(self):
        self.model = Sequential()

        # Build Convolutional / Pooling Layers
        self.model.add(Conv2D(filters=16,
                              kernel_size=(5, 5),
                              padding='same',
                              input_shape=(28, 28, 1),
                              activation='relu'))

        self.model.add(MaxPool2D(pool_size=(2, 2)))

        self.model.add(Conv2D(filters=36,
                              kernel_size=(5, 5),
                              padding='same',
                              activation='relu'))

        self.model.add(MaxPool2D(pool_size=(2, 2)))

        self.model.add(Dropout(0.25))

        # Build Backpropagation Neural Network
        self.model.add(Flatten())

        self.model.add(Dense(128, activation='relu'))
        self.model.add(Dropout(0.5))

        self.model.add(Dense(10, activation='softmax'))
        self.train_history = None

    def summary(self):
        print(self.model.summary())

    def training(self, x, y):
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.train_history = self.model.fit(x=x, y=y, validation_split=0.2, epochs=20, batch_size=300, verbose=2)

    def show_history(self, train_acc, test_acc):
        if self.train_history is not None:
            plt.plot(self.train_history.history[train_acc])
            plt.plot(self.train_history.history[test_acc])
            plt.title('Train History')
            plt.ylabel('Accuracy')
            plt.xlabel('Epoch')
            plt.legend(['train', 'test'], loc='upper left')
            plt.show()

    def save(self):
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M")
        self.model.save(dt_string + '.h5')



