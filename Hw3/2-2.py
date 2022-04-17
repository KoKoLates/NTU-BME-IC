import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline

# Activation Function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def prime_sigmoid(x):
    return x * (1 - x)

# Neural Network Model
def neural_network(epochs, eta):
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    t = np.array([[0], [1], [1], [0]])
    hidden_weights = np.array([[0.2, 0.2], [-0.4, -0.2]])
    hidden_bias = np.array([[-0.8, 0.1]])
    out_weights = np.array([[0.1], [-0.4]])
    out_bias = np.array([[-0.3]])

    data = []
    for _ in range(epochs):
        print()
        print("epochs:.{}".format(_ + 1))
        # Forward
        h_input = np.dot(x, hidden_weights)
        h_input += hidden_bias
        h_output = sigmoid(h_input)

        y_input = np.dot(h_output, out_weights)
        y_input += out_bias
        y_output = sigmoid(y_input)

        # Backward
        error = t - y_output
        data.append(abs(error))
        difference_value = error * prime_sigmoid(y_output)
        error_hidden_layer = difference_value.dot(out_weights.T)
        hidden_layer = error_hidden_layer * prime_sigmoid(h_output)

        out_weights += h_output.T.dot(difference_value) * eta
        out_bias += np.sum(difference_value, 0, keepdims=True) * eta
        hidden_weights += x.T.dot(hidden_layer) * eta
        hidden_bias += np.sum(hidden_layer, 0, keepdims=True) * eta
       
    
    # model = make_interp_spline(list(range(1, epochs + 1)), data)
    # xs = np.linspace(1, epochs)
    # ys = model(xs)
    # plt.plot(data, color='black')
    # plt.xlabel('epochs')
    # plt.ylabel('error')
    # plt.show()

    return hidden_weights, hidden_bias, out_weights, out_bias


def main():
    epochs, eta = 40000, 0.1
    hidden_weights, hidden_bias, out_weights, out_bias = neural_network(epochs, eta)


if __name__ == '__main__':
    main()
