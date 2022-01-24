import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from pyod.models.copod import COPOD
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.suod import SUOD
from sklearn.svm import OneClassSVM

if __name__ == '__main__':
    n_datapoints = 1000
    n_outliers = int(n_datapoints / 10)

    xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))
    test_data = np.random.standard_normal(n_datapoints).reshape((int(n_datapoints / 2), 2)) / 2
    outliers = np.random.uniform(low = -5, high = 5, size = n_outliers).reshape((int(n_outliers / 2), 2))

    test_data = np.concatenate([test_data, outliers])

    # initialized a group of outlier detectors for acceleration
    detector_list = [LOF(n_neighbors = 15), LOF(n_neighbors = 20), HBOS(n_bins = 10), HBOS(n_bins = 20),
                     COPOD(), IForest(n_estimators = 50), IForest(n_estimators = 100), IForest(n_estimators = 150)]

    # https://www.andrew.cmu.edu/user/yuezhao2/papers/21-mlsys-suod.pdf
    clf = SUOD(base_estimators = detector_list, n_jobs = 1, combination = 'average',
                    verbose = True)
    clf.fit(test_data)

    data_prediction = clf.decision_function(test_data)
    data_classes, confidence = clf.predict(test_data, return_confidence = True)

    dist_to_orig = np.linalg.norm(test_data, axis = 1)
    dist_to_orig_buckets = np.linspace(np.min(dist_to_orig), np.max(dist_to_orig), 25)
    bucket_counters = {bucket: dict(avg = 0, sum = 0, confidence = 0, probabilities = 0) for bucket in
                       dist_to_orig_buckets}


    def weiben(x, x_1, y_1, x_2, y_2):
        b = (np.log(-np.log(1 - y_2)) - np.log(-np.log(1 - y_1))) / (np.log(x_2) - np.log(x_1))
        a = x_1 * np.power(-np.log(1 - y_1), - 1 / b)

        return 1 - np.exp(-np.power(x / a, b))

    min_value = np.min(data_prediction)
    distance_to_min_value = np.abs(min_value - data_prediction)
    probabilities = weiben(distance_to_min_value, clf.threshold_, 0.1, distance_to_min_value.max(), 0.99)

    distances_to_center = np.linalg.norm(data_prediction, axis = 1)
    indexlist = np.argsort(distances_to_center)

    # for bucket_idx in range(len(dist_to_orig_buckets) - 1):
    #     data_idx = np.where(np.logical_and(dist_to_orig_buckets[bucket_idx] <= dist_to_orig,
    #                                        dist_to_orig < dist_to_orig_buckets[bucket_idx + 1]))
    #     if len(data_prediction[data_idx]) == 0:
    #         bucket_counters.pop(dist_to_orig_buckets[bucket_idx])
    #         continue
    #     bucket_counters[dist_to_orig_buckets[bucket_idx]]['avg'] = np.average(data_prediction[data_idx]).item()
    #     bucket_counters[dist_to_orig_buckets[bucket_idx]]['sum'] = np.sum(data_prediction[data_idx]).item()
    #     bucket_counters[dist_to_orig_buckets[bucket_idx]]['probabilities'] = np.average(probabilities[data_idx]).item()
    #     bucket_counters[dist_to_orig_buckets[bucket_idx]]['confidence'] = np.average(confidence[data_idx]).item()

    grid_points = np.c_[xx.ravel(), yy.ravel()]
    Z = clf.decision_function(grid_points)
    Z = Z.reshape(xx.shape)

    grid_points_on_threshold = grid_points[np.where(np.logical_and(
        np.linalg.norm(grid_points, axis = 1) > clf.threshold_ - 0.01,
        np.linalg.norm(grid_points, axis = 1) < clf.threshold_ + 0.01)
    )]

    # confidence = list(map(lambda value: value['confidence'], bucket_counters.values()))
    # probabilities = list(map(lambda value: value['probabilities'], bucket_counters.values()))
    plt.plot(distances_to_center[indexlist], confidence[indexlist], label = 'Confidence')
    # plt.plot(bucket_counters.keys(), probabilities, label = 'probabilities')
    plt.axvline(np.average(np.linalg.norm(grid_points_on_threshold, axis = 1)), 0, 1,
                label = 'Classification threshold', ls = '--', c = 'r')
    plt.ylabel("Classification confidence")
    plt.xlabel("Distance to the origin")
    plt.title("Outlier probability")
    plt.legend()
    plt.show()

    # fig = plt.figure(constrained_layout = True)
    # axd = fig.subplot_mosaic(
    #     """
    #     ACC
    #     BCC
    #     """
    # )
    #
    # avg_data = list(map(lambda value: value['avg'], bucket_counters.values()))
    # axd['A'].set_title('Average Distances')
    # axd['A'].bar(bucket_counters.keys(), avg_data, width=0.5)
    # axd['A'].set_xlabel('Distance to origin')
    # axd['A'].set_ylabel('Average distances to decision boundary')
    #
    # sum_data = list(map(lambda value: value['sum'], bucket_counters.values()))
    # axd['B'].set_title('Sum Distances')
    # axd['B'].bar(bucket_counters.keys(), sum_data, width=0.5)
    # axd['B'].set_xlabel('Distance to origin')
    # axd['B'].set_ylabel('Accumulated distances to decision boundary')
    #
    # axd['C'].set_title('Data')
    # grid_points = np.c_[xx.ravel(), yy.ravel()]
    # Z = clf.decision_function(grid_points)
    # Z = Z.reshape(xx.shape)
    #
    # grid_points_on_threshold = grid_points[np.where(np.logical_and(
    #     np.linalg.norm(grid_points, axis = 1) > clf.threshold_ - 0.1,
    #     np.linalg.norm(grid_points, axis = 1) < clf.threshold_ + 0.1)
    # )]
    # axd['B'].axvline(np.average(np.linalg.norm(grid_points_on_threshold, axis = 1)), 0, 1, label = 'Avg distance to origin of threshold', ls='--',  c = 'r')
    # axd['B'].axhline(clf.threshold_, 0, 1, label = 'Outlier Threshold', c = 'r')
    # axd['A'].axvline(np.average(np.linalg.norm(grid_points_on_threshold, axis = 1)), 0, 1, label = 'Avg distance to origin of threshold', ls='--',  c = 'r')
    # axd['A'].axhline(clf.threshold_, 0, 1, label = 'Outlier Threshold', c = 'r')
    # axd['A'].legend()
    # axd['B'].legend()
    #
    # axd['C'].contourf(xx, yy, Z, levels = np.linspace(Z.min(), clf.threshold_, 10), cmap = plt.cm.Reds_r)
    # axd['C'].contour(xx, yy, Z, levels = [clf.threshold_], linewidths = 2, colors = "darkred")
    # axd['C'].contourf(xx, yy, Z, levels = np.linspace(clf.threshold_, Z.max(), 10), cmap = plt.cm.PuBu)
    # axd['C'].scatter(test_data[:, 0], test_data[:, 1], c=['red' if data_class == 1 else 'blue' for data_class in data_classes])
    # legend_elements = [Line2D([], [], marker = 'o', color = None, label = 'Inlier', markerfacecolor = 'b', linestyle='None'),
    #                    Line2D([], [], marker = 'o', color = None, label = 'Outlier', markerfacecolor = 'r', linestyle='None')]
    #
    # axd['C'].legend(handles=legend_elements, loc = 'upper left')
    # plt.show()
