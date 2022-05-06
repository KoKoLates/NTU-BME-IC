import keras.models
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import DataSet

model = keras.models.load_model('202205061402.h5')

# scores = model.evaluate(DataSet.x_test, DataSet.y_test)
# print(scores[1])
predictions = np.argmax(model.predict(DataSet.x_test), axis=1)
print(predictions[:10])


def plot_images_labels_prediction(images, labels, prediction, idx, num=10):
    fig = plt.gcf()
    fig.set_size_inches(12, 14)
    if num > 25:
        num = 25
    for i in range(0, num):
        ax = plt.subplot(5, 5, 1 + i)
        ax.imshow(images[idx], cmap='binary')

        ax.set_title("label=" + str(labels[idx]) +
                     ",predict=" + str(prediction[idx])
                     , fontsize=10)

        ax.set_xticks([])
        ax.set_yticks([])
        idx += 1
    plt.show()


plot_images_labels_prediction(DataSet.x_test, DataSet.y_test, predictions, idx=0)

pd.crosstab(DataSet.y_test, predictions, rownames=['label'], colnames=['predict'])
df = pd.DataFrame({'label': DataSet.y_test, 'predict': predictions})
print(df[(df.label == 5) & (df.predict == 3)])
