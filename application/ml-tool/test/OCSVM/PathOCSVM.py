from tqdm.auto import tqdm

from test.TestUtils import create_path_sets
import itertools
from sklearn.svm import OneClassSVM
import numpy as np


def set_kernel(X: np.ndarray, Y: np.ndarray):
    gram_matrix = np.ndarray((X.shape[0], Y.shape[0]))

    for i, j in itertools.combinations_with_replacement(range(X.shape[0]), 2):
        matching = 0
        vec_one = np.trim_zeros(X[i])
        vec_two = np.trim_zeros(Y[c])

        for x, y in itertools.product(vec_one, vec_two):
            matching += 1 if x == y else 0

        gram_matrix[i, c] = matching
        gram_matrix[c, i] = matching

    return gram_matrix


if __name__ == '__main__':


    path_sets = create_path_sets(trim_data = -1)
    folder_path = list(map(lambda my_set: list(map(lambda my_list: my_list[-2], my_set)), path_sets))

    vocab = []
    for folders in folder_path:
        for folder in folders:
            if folder not in vocab:
                vocab.append(folder)

    vec_length = max(map(len, folder_path))

    test_matrix = []
    for folders in folder_path:
        vector = np.zeros(vec_length, dtype = np.int32)
        for idx, folder in enumerate(folders):
            vector[idx] = vocab.index(folder) + 1
        test_matrix.append(vector)

    test_matrix = np.asarray(test_matrix)

    train_set = test_matrix[:int((len(test_matrix) + 1) * .80)]
    test_set = test_matrix[int((len(test_matrix) + 1) * .80):]

    clf = OneClassSVM(kernel = set_kernel)
    clf.fit(train_set)
