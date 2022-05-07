import Model


def main():
    model = Model.Model()
    model.summary()
    model.train()
    model.save()
    model.show_history('Accuracy', 'accuracy', 'val_accuracy')
    model.show_history('Loss', 'loss', 'val_loss')


if __name__ == '__main__':
    main()
