import matplotlib
import matplotlib.pyplot as plt
from pyod.utils.data import generate_data, generate_data_clusters
import numpy as np

if __name__ == '__main__':

    # Generate sample data
    # x_train, x_test, y_train, y_test = generate_data_clusters(n_clusters = 5)
    x_train, x_test, y_train, y_test = generate_data(behaviour = 'new', offset = 20)

    outliers = x_train[y_train == 0]
    inliers = x_train[y_train == 1]


    subplot = plt.subplot(1, 1, 1)

    b = subplot.scatter(outliers[:, 0], outliers[:, 1], c = 'white', s = 20, edgecolor = 'k')
    c = subplot.scatter(inliers[:, 0], inliers[:, 1], c = 'black', s = 20, edgecolor = 'k')

    subplot.axis('tight')
    subplot.legend(
        [b, c],
        ['true inliers', 'true outliers'],
        prop = matplotlib.font_manager.FontProperties(size = 10),
        loc = 'lower right')
    plt.show()