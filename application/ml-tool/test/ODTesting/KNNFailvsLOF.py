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
    theta = np.radians(30)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    test_data2_circle = R

    xx, yy = np.meshgrid(np.linspace(-1, 1, 10), np.linspace(-1, 1, 10))
    test_data1 = np.c_[xx.ravel(), yy.ravel()]
    test_data1_circle = test_data1[np.where(np.linalg.norm(test_data1, axis = 1) < 1)]
    test_data1_circle_rotate = np.tensordot(test_data1_circle, R, axes=([1], [0])) - 3

    xx, yy = np.meshgrid(np.linspace(-1, 1, 10), np.linspace(-1, 1, 10))
    test_data2 = np.c_[xx.ravel(), yy.ravel()]
    test_data2_circle = test_data2[np.where(np.linalg.norm(test_data2, axis = 1) < 0.8)]
    test_data2_circle_rotate = np.tensordot(test_data2_circle, R, axes=([1], [0])) * 3 + 3

    test_data = np.concatenate([test_data1_circle_rotate, test_data2_circle_rotate, np.asarray([[-1.9, -1.9]])])

    lof = LOF()
    lof.fit(test_data)

    knn = KNN()
    knn.fit(test_data)

    data_prediction = lof.decision_function(test_data)
    data_classes = lof.predict(test_data)

    data_prediction2 = knn.decision_function(test_data)
    data_classes2 = knn.predict(test_data)

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 2)
    ax2 = fig.add_subplot(1, 2, 1)

    ax1.set_title('LOF', fontsize=20)
    ax2.set_title('KNN', fontsize=20)

    xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))
    inliers = data_prediction[np.where(data_classes == 0)]
    outliers = data_prediction[np.where(data_classes == 1)]
    Z = lof.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax1.contourf(xx, yy, Z, levels = np.linspace(Z.min(), outliers.min(), 10), cmap = plt.cm.Reds_r)
    ax1.contour(xx, yy, Z, levels = [outliers.min()], linewidths = 2, colors = "darkred")
    ax1.contourf(xx, yy, Z, levels = np.linspace(outliers.min(), Z.max(), 7), cmap = plt.cm.PuBu)

    xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))
    inliers = data_prediction[np.where(data_classes2 == 0)]
    outliers = data_prediction[np.where(data_classes2 == 1)]
    Z = knn.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    ax2.contourf(xx, yy, Z, levels = np.linspace(Z.min(), outliers.min(), 10), cmap = plt.cm.Reds_r)
    ax2.contour(xx, yy, Z, levels = [outliers.min()], linewidths = 2, colors = "darkred", label = "Decision boundary")
    ax2.contourf(xx, yy, Z, levels = np.linspace(outliers.min(), Z.max(), 7), cmap = plt.cm.PuBu)

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
    ax1.set_xlim(left = -5, right = 5)
    ax2.set_xlim(left = -5, right = 5)
    ax1.set_ylim(bottom = -5, top = 5)
    ax2.set_ylim(bottom = -5, top = 5)

    plt.show()
