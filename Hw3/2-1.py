import numpy as np
from itertools import product, cycle
from matplotlib import pyplot as plt


def main():
    x = cycle(product((-1, 1), (-1, 1)))
    out_weight = np.array((1, -1, 0), dtype=np.float64)
    t = cycle((0, 1, 1, 0))
    eta = 0.1
    data = []

    for i, (x, t) in enumerate(zip(x, t)):
        if i % 4 == 0:
            print()
            print("epochs:{}".format(i // 4 + 1))
        if i == 100:
            break

        x = np.array((*x, -1))
        a = np.dot(out_weight, x)
        y = 1 if a > 0 else 0
        dw = eta * (t - y) * x
        data.append(t - y)
        # print("w1:{} w2:{}".format(w[0], w[1]))
        print(x)

        out_weight += dw

    plt.xlabel("epochs")
    plt.ylabel("error")
    plt.plot(data, color='black')
    plt.show()


if __name__ == '__main__':
    main()
