import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from pyod.models.cof import COF
from pyod.models.hbos import HBOS
from pyod.models.knn import KNN
from pyod.models.lof import LOF
from pyod.models.ocsvm import OCSVM
from pyod.models.pca import PCA

if __name__ == '__main__':
    n_datapoints = 1000
    n_outliers = int(n_datapoints / 10)

    test_data = np.column_stack([np.linspace(-4, 4, 11), np.zeros(11)])
    outlier = np.asarray([[0, 1]])

    test_data = np.concatenate([test_data, outlier])

    cof = COF(n_neighbors=4)
    cof.fit(test_data)

    lof = LOF(n_neighbors=4)
    lof.fit(test_data)

    data_prediction = lof.decision_function(test_data)
    data_classes = lof.predict(test_data)

    data_prediction2 = cof.decision_function(test_data)
    data_classes2 = cof.predict(test_data)

    print(data_classes)
    print(data_classes2)

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ax1.set_title('LOF')
    ax2.set_title('COF')

    ax1.scatter(test_data[:, 0],
               test_data[:, 1],
               c = ['red' if data_class == 1 else 'blue' for data_class in data_classes],
               label = ['Outlier' if data_class == 1 else 'Inlier' for data_class in data_classes]
           )

    ax2.scatter(test_data[:, 0],
               test_data[:, 1],
               c = ['red' if data_class == 1 else 'blue' for data_class in data_classes2],
               label = ['Outlier' if data_class == 1 else 'Inlier' for data_class in data_classes2]
           )

    legend_elements = [Line2D([], [], marker = 'o', color = None, label = 'Inlier', markerfacecolor = 'b', linestyle='None'),
                       Line2D([], [], marker = 'o', color = None, label = 'Outlier', markerfacecolor = 'r', linestyle='None')]

    ax1.legend(handles=legend_elements, loc = 'upper left')
    ax2.legend(handles=legend_elements, loc = 'upper left')
    plt.show()
