import itertools

import numpy as np
import scipy
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import OneClassSVM
from tqdm.auto import tqdm

import math

from src.Exceptions import DataNotLoaded, OCSVMNotTrained
import pickle

from src.loader.database.dbmodels.FileServerModel import FileServerModel


class PathOCSVM:
    def __init__(self, path_sets = None, data_index = -2):
        self.occurrence_vectorized = np.vectorize(PathOCSVM.count_occurrence, excluded = ['comp_vec'])
        self.path_sets = path_sets
        self.train_sets = []

        # Elements that are stored in the data base per file server basis
        self.vocab = []
        self.svm = OneClassSVM(kernel = 'precomputed', gamma = 'scale', verbose= True)
        self.scaler = MinMaxScaler()
        self.train_matrix = None

        # The data index describes which element of the path to use in the classification
        self.data_index = data_index
        pass

    def fit(self):
        # todo this step should not be necessary every time only on "retrain"
        self.train_sets = self.preprocess()
        self.calculate_vocab()

        self.train_matrix = self.data_index_transformation()
        train_gram_matrix = self.precompute(self.train_matrix, self.train_matrix, fit = True)
        self.scaler.fit(train_gram_matrix)
        transformed_train_gram_matrix = self.scaler.transform(train_gram_matrix)
        self.svm.fit(transformed_train_gram_matrix)

    def predict(self, test_data = None):
        if self.train_matrix is None:
            raise OCSVMNotTrained("OCSVM is not trained. \nEither Load data or train.")

        test_set = self.preprocess(test_data)
        self.calculate_vocab(test_set)
        test_matrix = self.data_index_transformation(test_set)
        test_gram_matrix = self.precompute(test_matrix, self.train_matrix)
        transformed_test_gram_matrix = self.scaler.transform(test_gram_matrix)

        test_dec = self.svm.decision_function(transformed_test_gram_matrix)

        return 1 - (1 / np.sqrt(np.abs(test_dec)))

    def preprocess(self, path_sets = None):
        # Check which parameter to use
        if path_sets is None:
            path_sets = self.path_sets

        # Check if there is data available
        if path_sets is None:
            raise DataNotLoaded('Path sets are empty')

        data_sets = []

        # Get the specific path index given through data index
        for path_set in path_sets:
            folder_set = []
            for path in path_set:
                # todo think about what happens when the index is out of range
                folder_set.append(path[self.data_index])

            folder_set = np.asarray(folder_set)
            data_sets.append(folder_set)

        return data_sets

    def calculate_vocab(self, element_sets = None):
        if element_sets is None:
            element_sets = self.train_sets

        for elements in element_sets:
            unique_elements = np.unique(elements)
            for element in unique_elements:
                if element not in self.vocab:
                    self.vocab.append(element)
        return self.vocab

    def data_index_transformation(self, element_sets = None):
        # Check which parameter to use
        if element_sets is None:
            element_sets = self.train_sets

        data_matrix = []
        # Transform the elements in the train sets into indexes given by the vocabulary
        for train_set in element_sets:
            data_matrix.append(
                np.where(train_set.reshape(train_set.size, 1) == self.vocab)[1]
            )
        return data_matrix

    def get_stored_model(self):
        return dict(
            svm = pickle.dumps(self.svm),
            scaler = pickle.dumps(self.scaler),
            train_matrix = list(map(lambda x: x.tolist(), self.train_matrix)),
            vocab = self.vocab
        )

    def load_stored_model(self, fileServerModel: FileServerModel):
        stored_svm = fileServerModel.svm

        svm = stored_svm['svm']
        scaler = stored_svm['scaler']
        train_matrix = stored_svm['train_matrix']
        vocab = stored_svm['vocab']

        self.svm = pickle.loads(svm)
        self.scaler = pickle.loads(scaler)
        self.train_matrix = list(map(lambda x: np.asarray(x), train_matrix))
        self.vocab = vocab

    @staticmethod
    def count_occurrence(element, comp_vec):
        return np.count_nonzero(comp_vec == element)

    def precompute(self, X, Y, fit = False):
        gram_dimensions = (len(X), len(Y))
        gram_matrix = np.zeros(gram_dimensions, dtype = np.float64)

        # print(f'X.shape {X.shape} Y.shape {Y.shape}')
        if fit:
            total = scipy.special.comb(len(X), 2, exact = True)
            for i, j in tqdm(itertools.combinations_with_replacement(range(len(X)), 2), desc = "Precompute:",
                             total = int(total)):
                matching = self.occurrence_vectorized(X[i], comp_vec = Y[j]).sum()

                gram_matrix[i, j] = matching
                gram_matrix[j, i] = matching

            return gram_matrix
        else:
            for i, j in itertools.product(range(len(X)), range(len(Y))):
                gram_matrix[i, j] = self.occurrence_vectorized(X[i], comp_vec = Y[j]).sum()

            return gram_matrix