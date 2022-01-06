import itertools
from typing import Optional, Dict

import numpy as np
import scipy
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import OneClassSVM
from tqdm.auto import tqdm

import math

from src.Exceptions import DataNotLoaded, OCSVMNotTrained, NotInitializedException
import pickle

from src.loader.database.dbmodels.IFileServerModel import IFileServerModel
from src.utils import Constants


class PathOCSVM:
    def __init__(self, path_separator = "/", data_index = -2):
        self.occurrence_vectorized = np.vectorize(PathOCSVM.count_occurrence, excluded = ['comp_vec'])
        self.train_sets = []

        # Elements that are stored in the data base per file server basis
        self.vocab = []
        self.svm = None
        self.scaler = None
        self.train_matrix = None
        self.trained_gram_matrix = None
        self.distances = None

        # The data index describes which element of the path to use in the classification
        self.path_separator = path_separator
        self.data_index = data_index
        self.initialized = False

    def initialize_model(self, stored_data: Optional[Dict] = None):
        if stored_data:
            svm = stored_data['svm']
            scaler = stored_data['scaler']
            train_matrix = stored_data['train_matrix']
            vocab = stored_data['vocab']
            distances = stored_data['distances']
            trained_gram_matrix = stored_data['trained_gram_matrix']

            self.svm = pickle.loads(svm)
            self.scaler = pickle.loads(scaler)
            self.train_matrix = list(map(lambda x: np.asarray(x), train_matrix))
            self.trained_gram_matrix = pickle.loads(trained_gram_matrix)
            self.vocab = vocab
            self.distances = distances
        else:
            self.svm = OneClassSVM(
                nu = 0.15,
                kernel = 'precomputed',
                gamma = 'scale',
                verbose = Constants.verbose_printing,
                max_iter = 2000
            )
            self.scaler = MinMaxScaler(feature_range=(-1, 1))

        self.initialized = True

    def fit(self, backup_data_list):
        if not self.initialized:
            raise NotInitializedException('The meta data model is not initialized')

        self.train_sets = self.preprocess(backup_data_list)
        self.calculate_vocab()

        self.train_matrix = self.data_index_transformation()
        self.trained_gram_matrix = self.precompute(self.train_matrix, self.train_matrix, fit = True)
        self.scaler.fit(self.trained_gram_matrix)
        transformed_train_gram_matrix = self.scaler.transform(self.trained_gram_matrix)
        self.svm.fit(transformed_train_gram_matrix)
        self.distances = list(self.svm.decision_function(self.trained_gram_matrix))

    def predict(self, test_backup_data, continues_training = True):
        if not self.initialized:
            raise NotInitializedException('The meta data model is not initialized')

        if self.train_matrix is None:
            raise OCSVMNotTrained("OCSVM is not trained. \nEither Load data or train.")

        test_set = self.preprocess(test_backup_data)
        self.calculate_vocab(test_set)
        test_matrix = self.data_index_transformation(test_set)
        test_gram_matrix = self.precompute(test_matrix, self.train_matrix)
        transformed_test_gram_matrix = self.scaler.transform(test_gram_matrix)
        test_dec = self.svm.decision_function(transformed_test_gram_matrix)

        complete_distances = [element for element in self.distances]
        complete_distances.append(test_dec.item())

        max_value = np.max(complete_distances)
        distance_to_max = np.abs(max_value - complete_distances)

        if continues_training:
            if Constants.verbose_printing:
                print('Path OCSVM continues training')

            self.add_vec_to_gram(test_gram_matrix, test_matrix)
            self.scaler.fit(self.trained_gram_matrix)
            transformed_train_gram_matrix = self.scaler.transform(self.trained_gram_matrix)
            if Constants.verbose_printing:
                print(transformed_train_gram_matrix.shape)
            self.svm.fit(transformed_train_gram_matrix)
            self.distances = list(self.svm.decision_function(self.trained_gram_matrix))

        return list(np.nan_to_num(1 - 1 / np.sqrt(distance_to_max), neginf = 0))

    def preprocess(self, backup_data_list):

        # Check if there is data available
        if backup_data_list is None or len(backup_data_list) == 0:
            raise DataNotLoaded('Path sets are empty')

        path_sets = list(list(map(lambda x: x[Constants.name_index], backup_data)) for backup_data in backup_data_list)

        data_sets = []

        # Get the specific path index given through data index
        for paths in path_sets:
            folder_set = []
            for path in paths:
                path_set = path.split(self.path_separator)
                # todo think about what happens when the index is out of range
                if len(path_set) < -self.data_index:
                    folder_set.append('root')
                else:
                    folder_set.append(path_set[self.data_index])

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

    @staticmethod
    def count_occurrence(element, comp_vec):
        return np.count_nonzero(comp_vec == element)

    def add_vec_to_gram(self, test_gram_matrix, test_matrix):
        gram_matrix = self.precompute(test_matrix, test_matrix, fit = True)
        next_gram_matrix = np.row_stack([self.trained_gram_matrix, test_gram_matrix])
        next_column = np.column_stack([test_gram_matrix, gram_matrix]).T
        self.trained_gram_matrix = np.column_stack([next_gram_matrix, next_column])

        for test_array in test_matrix:
            self.train_matrix.append(test_array)

    def precompute(self, X, Y, fit = False):
        gram_dimensions = (len(X), len(Y))
        gram_matrix = np.zeros(gram_dimensions, dtype = np.float64)

        # print(f'X.shape {X.shape} Y.shape {Y.shape}')
        if fit:
            total = scipy.special.comb(len(X), 2, exact = True)

            if Constants.verbose_printing:
                next_iter = tqdm(itertools.combinations_with_replacement(range(len(X)), 2), desc = "Precompute:",
                             total = int(total))
            else:
                next_iter = itertools.combinations_with_replacement(range(len(X)), 2)

            for i, j in next_iter:
                matching = self.occurrence_vectorized(X[i], comp_vec = Y[j]).sum()

                gram_matrix[i, j] = matching
                gram_matrix[j, i] = matching

            return gram_matrix
        else:
            for i, j in itertools.product(range(len(X)), range(len(Y))):
                gram_matrix[i, j] = self.occurrence_vectorized(X[i], comp_vec = Y[j]).sum()

            return gram_matrix


