import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.knn import KNN
from pyod.models.loci import LOCI
from pyod.models.lof import LOF
from pyod.models.ocsvm import OCSVM
from pyod.models.pca import PCA
from pyod.models.auto_encoder import AutoEncoder

if __name__ == '__main__':
    n_datapoints = 1000
    n_outliers = int(n_datapoints / 10)

    xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))
    test_data = np.random.standard_normal(n_datapoints // 2).reshape((int(n_datapoints / 4), 2)) / 2 - 2
    test_data2 = np.random.standard_normal(n_datapoints // 4).reshape((int(n_datapoints / 8), 2)) / 2 + 2
    test_data3 = np.random.standard_normal(20).reshape((int(20 / 2), 2)) / 2 + np.asarray([+2, -2])
    outliers = np.random.uniform(low = -5, high = 5, size = n_outliers).reshape((int(n_outliers / 2), 2))

    test_data = np.concatenate([test_data, test_data2, test_data3, outliers])

    clf = AutoEncoder(epochs=300, hidden_neurons = [2, 32, 32, 2])
    clf.fit(test_data)

    data_prediction = clf.decision_function(test_data)
    data_classes = clf.predict(test_data)

    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    inliers = data_prediction[np.where(data_classes == 0)]
    outliers = data_prediction[np.where(data_classes == 1)]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('KNN on standard deviation')
    ax.contourf(xx, yy, Z, levels = np.linspace(Z.min(), outliers.min(), 10), cmap = plt.cm.Reds_r)
    ax.contour(xx, yy, Z, levels = [outliers.min()], linewidths = 2, colors = "darkred")
    ax.contourf(xx, yy, Z, levels = np.linspace(outliers.min(), Z.max(), 7), cmap = plt.cm.PuBu)
    ax.scatter(test_data[:, 0],
               test_data[:, 1],
               c = ['red' if data_class == 1 else 'blue' for data_class in data_classes],
               label = ['Outlier' if data_class == 1 else 'Inlier' for data_class in data_classes]
               )

    legend_elements = [Line2D([], [], marker = 'o', color = None, label = 'Inlier', markerfacecolor = 'b', linestyle='None'),
                       Line2D([], [], marker = 'o', color = None, label = 'Outlier', markerfacecolor = 'r', linestyle='None')]

    ax.legend(handles=legend_elements, loc = 'upper left')
    plt.show()
