import DataSet
import keras.models
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


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
        label_name = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        df_cm = pd.DataFrame(confusion_matrix(self.y_test, self.predictions), index=label_name, columns=label_name)
        fig = plt.figure(figsize=(10, 7))
        try:
            heatmap = sns.heatmap(df_cm, annot=True, fmt='d', linewidths=1.5, cmap='PuBuGn')
        except ValueError:
            raise ValueError('Confusion matrix values should be integers')

        heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=10)
        heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=0, ha='right', fontsize=10)
        plt.ylabel('True Labels')
        plt.xlabel('Predicted Labels')
        plt.show()


def main():
    model = keras.models.load_model('202205061402.h5')
    test = Test(model)
    test.confusion_matrix()
    # test.score()
    # test.predictions()


if __name__ == '__main__':
    main()
