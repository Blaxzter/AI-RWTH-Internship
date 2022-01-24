import pickle

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

if __name__ == '__main__':
    with open('data/gram_matrix.pickle', 'rb') as handle:
        gram_matrix = np.asarray(pickle.load(handle))

    with open('data/one_prediction.pickle', 'rb') as handle:
        one_prediction = pickle.load(handle)

    fig, ax = plt.subplots()

    print("Average of negative: ", np.average(gram_matrix[np.where(np.asarray(one_prediction['path_ocsvm'][0]) == 0)]))
    print("Average of positive: ", np.average(gram_matrix[np.where(np.asarray(one_prediction['path_ocsvm'][0]) == 1)]))

    plt.plot(np.arange(0, gram_matrix.shape[0]), np.average(np.asarray(gram_matrix), 0))
    plt.show()
