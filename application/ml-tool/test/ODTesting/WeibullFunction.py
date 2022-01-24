
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    def weiben(x, x_1, y_1, x_2, y_2):
        b = (np.log(-np.log(1 - y_2)) - np.log(-np.log(1 - y_1))) / (np.log(x_2) - np.log(x_1))
        a = x_1 * np.power(-np.log(1 - y_1), - 1 / b)

        return 1 - np.exp(-np.power(x / a, b))

    x = np.linspace(0, 12, 1000)
    _x_1 = 2
    _x_2 = 9
    _y_1 = 0.1
    _y_2 = 0.9
    data = weiben(x, _x_1, _y_1, _x_2, _y_2)

    plt.plot(x, data)

    plt.axhline(y = _y_1, xmin = 0, xmax = _x_1 / 12, color = 'g')
    plt.axvline(x = _x_1, ymin = 0, ymax = np.abs(-_y_1 - _y_1) / 1.2, color = 'g')
    plt.text(3.3, 0.08, r'$(x_1, y_1)$', fontsize = 18)
    plt.scatter(x = [_x_1], y = [_y_1], marker = 'x', color = 'g', s = 100)

    plt.axhline(y = _y_2, xmin = 0, xmax = _x_2 / 12, color = 'r')
    plt.axvline(x = _x_2, ymin = 0, ymax = np.abs(-_y_1 - _y_2) / 1.2, color = 'r')
    plt.text(_x_2, 0.85, r'$(x_2, y_2)$', fontsize = 18)
    plt.scatter(x = [_x_2], y = [_y_2], marker = 'x', color = 'r', s = 100)

    plt.xlim(left = 0, right = 12)
    plt.ylim(bottom = -_y_1, top = 1.1)
    plt.xlabel("Distance to smallest outlier score")
    plt.ylabel("Outlier probability")
    plt.title("Weibull cumulative distribution function.")
    plt.show()