import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# Activation Funciton
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def prime_sigmoid(x):
    return x * (1 - x)

# Neural Netwowrk Model
def neural_network(epochs, eta):
    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    t = np.array([[0], [1], [1], [0]])
    hidden_weight = np.array([[0.2], [-0.4]])
    hidden_bias = np.array([[-0.8]])
    out_weight = np.array([[0.2], [-0.2], [-0.4]])
    out_bias = np.array([[-0.3]])

    data = []
    for _ in range(epochs):
        print()
        print("epochs:.{}".format(_ + 1))
        # Forward
        h_input = np.dot(x, hidden_weight)
        h_input += hidden_bias
        h_output = np.column_stack((x, sigmoid(h_input)))

        y_input = np.dot(h_output, out_weight)
        y_input += out_bias
        y_output = sigmoid(y_input)

        # Backward
        error = t - y_output
        data.append(abs(error))
        d2 = error * prime_sigmoid(y_output)
        error_hidden_layer = d2.dot(out_weight.T)
        d1 = (error_hidden_layer * prime_sigmoid(h_output))[0:4, 2:3]

        out_weight += h_output.T.dot(d2) * eta
        out_bias += np.sum(d2, axis=0, keepdims=True) * eta
        hidden_weight += (x.T.dot(d1) * eta)
        hidden_bias += (np.sum(d1, axis=0, keepdims=True) * eta)

    # model = make_interp_spline(list(range(1, epochs + 1)), data)
    # xs = np.linspace(1, epochs)
    # ys = model(xs)
    # plt.plot(data, color='black')
    # plt.xlabel('epochs')
    # plt.ylabel('error')
    # plt.show()

    return hidden_weight, hidden_bias, out_weight, out_bias


def main():
    epochs, eta = 40000, 0.1
    hidden_weights, hidden_bias, out_weights, out_bias = neural_network(epochs, eta)


if __name__ == '__main__':
    main()

