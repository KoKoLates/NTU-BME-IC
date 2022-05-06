import Model
import DataSet


def main():
    model = Model.Model()
    model.summary()
    model.training(DataSet.x_train, DataSet.y_train)
    model.save()

    # model.show_history('accuracy', 'val_accuracy')
    # model.show_history('loss', 'val_loss')


if __name__ == '__main__':
    main()
