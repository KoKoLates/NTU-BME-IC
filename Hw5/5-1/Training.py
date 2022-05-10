import Model
import DataSet


def main():
    data = DataSet.DataSet()
    x_train, y_train = data.train_data()
    model = Model.Model()
    model.summary()
    model.training(x_train, y_train)
    model.save()

    # model.show_history('accuracy', 'val_accuracy')
    # model.show_history('loss', 'val_loss')


if __name__ == '__main__':
    main()
