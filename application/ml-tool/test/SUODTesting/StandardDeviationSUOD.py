import matplotlib.pyplot as plt
import numpy as np
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
    data_classes = clf.predict(test_data)

    dist_to_orig = np.linalg.norm(test_data, axis = 1)
    dist_to_orig_buckets = np.linspace(np.min(dist_to_orig), np.max(dist_to_orig), 25)
    bucket_counters = {bucket: dict(avg = 0, sum = 0) for bucket in dist_to_orig_buckets}

    for bucket_idx in range(len(dist_to_orig_buckets) - 1):
        data_idx = np.where(np.logical_and(dist_to_orig_buckets[bucket_idx] <= dist_to_orig,
                                           dist_to_orig < dist_to_orig_buckets[bucket_idx + 1]))
        if len(data_prediction[data_idx]) == 0:
            bucket_counters.pop(dist_to_orig_buckets[bucket_idx])
            continue
        bucket_counters[dist_to_orig_buckets[bucket_idx]]['avg'] = np.average(data_prediction[data_idx]).item()
        bucket_counters[dist_to_orig_buckets[bucket_idx]]['sum'] = np.sum(data_prediction[data_idx]).item()

    fig = plt.figure(constrained_layout = True)
    axd = fig.subplot_mosaic(
        """
        ACC
        BCC
        """
    )

    avg_data = list(map(lambda value: value['avg'], bucket_counters.values()))
    axd['A'].set_title('Average Distances')
    axd['A'].bar(bucket_counters.keys(), avg_data, width=0.5)
    axd['A'].set_xlabel('Distance to x axis')
    axd['A'].set_ylabel('Average distances to decision boundary')

    sum_data = list(map(lambda value: value['sum'], bucket_counters.values()))
    axd['B'].set_title('Sum Distances')
    axd['B'].bar(bucket_counters.keys(), sum_data, width=0.5)
    axd['B'].set_xlabel('Distance to x axis')
    axd['B'].set_ylabel('Accumulated distances to decision boundary')

    axd['C'].set_title('Data')
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    axd['C'].contourf(xx, yy, Z, levels = np.linspace(Z.min(), 0, 10), cmap = plt.cm.PuBu)
    axd['C'].contour(xx, yy, Z, levels = [0], linewidths = 2, colors = "darkred")
    axd['C'].contourf(xx, yy, Z, levels = np.linspace(0, Z.max(), 7), cmap = plt.cm.Reds_r)
    axd['C'].scatter(test_data[:, 0], test_data[:, 1], c=['red' if data_class == 1 else 'blue' for data_class in data_classes])
    plt.show()
