import time

import numpy as np
from dateutil.parser import parse
from pyod.models.copod import COPOD
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.suod import SUOD
from sklearn import preprocessing

from src.loader.FileDatabase import FileDatabase
from src.utils.Constants import action_index, date_index

class FileFeatureModel:

    def __init__(self, train_data = None, file_data_base = None):
        self.train_data = train_data
        self.file_data_base = file_data_base

        # initialized a group of outlier detectors for acceleration
        detector_list = [LOF(n_neighbors = 15), LOF(n_neighbors = 20),
                         LOF(n_neighbors = 25), LOF(n_neighbors = 35),
                         COPOD(), IForest(n_estimators = 100),
                         IForest(n_estimators = 200)]
        # https://www.andrew.cmu.edu/user/yuezhao2/papers/21-mlsys-suod.pdf
        self.clf = SUOD(base_estimators = detector_list, n_jobs = 2, combination = 'average', verbose = False)

    def fit(self):
        pass

    def parse_features(self, backup_data):
        file_features = []

        for file_data in backup_data:
            file_name = file_data[1]
            action, name, user, date = file_data

            # Check if the file is in the database
            if file_name not in self.file_data_base:
                # Create a new entry in the file feature vector
                file_features.append(dict(
                    name = name,
                    action_date = date,
                    action = action,
                    user = user,
                    user_difference = 0,
                    frequency = 0,
                    amount = 0,
                    time_since_last_use = 0,
                ))
            else:
                # create a file vector based
                file_history = self.file_data_base.get_file_history(name)

                # Get the meta data over the file history
                amount = len(file_history)
                current_date = parse(date)
                time_since_last_use = parse(file_history[-1]['action_date']) - current_date
                date_range = parse(file_history[0]['action_date']) - current_date

                user_difference = 0 if file_history[-1]['user'] == user else 1

                file_features.append(dict(
                    name = name,
                    action_date = date,
                    action = action,
                    user = user,
                    user_difference = user_difference,
                    frequency = amount / date_range.total_seconds(),
                    amount = amount,
                    time_since_last_use = time_since_last_use.total_seconds(),
                ))

