import keras.models
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import DataSet


class Test:
    def __init__(self, model):
        self.model = model
        data = DataSet.DataSet()
        (self.x_test, self.y_test), (self.x_test_processed, self.y_test_processed) = data.test_date()
        self.predictions = np.argmax(self.model.predict(self.x_test), 1)

    def score(self):
        scores = self.model.evaluate(self.x_test_processed, self.y_test_processed)
        print('Accuracy -> {}'.format(scores[1]))

    def predictions(self):
        def plot_predictions(images, labels, prediction, index, num):
            fig = plt.gcf()
            fig.set_size_inches(12, 14)
            if num > 25:
                num = 25

            for i in range(0, num):
                ax = plt.subplot(5, 5, 1 + i)
                ax.imshow(images[index], cmap='binary')
                ax.set_title('label:{} / predict:{}'.format(str(labels[index]), str(prediction[index])), fontsize=9)
                ax.set_xticks([])
                ax.set_yticks([])
                index += 1

            plt.show()

        plot_predictions(self.x_test, self.y_test, self.predictions, 0, 10)

    def confusion_matrix(self):
        print(pd.crosstab(self.y_test, self.predictions, rownames=['label'], colnames=['predict']))


def main():
    model = keras.models.load_model('202205061402.h5')
    test = Test(model)
    test.confusion_matrix()
    # test.score()
    # test.predictions()


if __name__ == '__main__':
    main()
