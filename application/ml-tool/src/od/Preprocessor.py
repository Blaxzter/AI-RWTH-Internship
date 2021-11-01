import time

import numpy as np
from dateutil.parser import parse
from sklearn import preprocessing

from src.loader.FileDatabase import FileDatabase
from src.utils.Constants import action_index, date_index

unix_date_scaler = preprocessing.MinMaxScaler()


def get_backup_meta_data(backed_up_files):
    backed_up_amount = len(backed_up_files)

    # Get the actions and counts of each action
    action_list = list(map(lambda d: d[action_index], backed_up_files))
    uniques, counts = np.unique(action_list, return_counts = True)

    # Get the mean and std deviation of the min max scaled date range of all changes
    parse_access_dates = list(map(lambda d: parse(d[date_index]), backed_up_files))
    unix_dates = np.array(list(map(lambda date: time.mktime(date.timetuple()), parse_access_dates)))
    unix_dates = unix_dates.reshape(-1, 1)
    unix_dates_scaled = unix_date_scaler.fit_transform(unix_dates)

    unix_dates_mean = np.mean(unix_dates_scaled)
    unix_dates_std = np.std(unix_dates_scaled)

    # Get the date ranges in unix time stamps
    sorted_access_dates = sorted(unix_dates)
    earliest_date = sorted_access_dates[0]
    latest_date = sorted_access_dates[-1]
    return dict(
        backed_up_amount = backed_up_amount,
        uniques_counts = dict(uniques = uniques.tolist(), counts = counts.tolist()),
        date_range = dict(earliest_date = earliest_date.item(), latest_date = latest_date.item()),
        date_mean_std = dict(unix_dates_mean = unix_dates_mean, unix_dates_std = unix_dates_std)
    )


def parse_feature_data(backed_up_files, file_database):
    backup_meta_data = get_backup_meta_data(backed_up_files)

    current_file_database = FileDatabase(file_database, is_sorted = True)

    file_features = []

    for file_data in backed_up_files:
        file_name = file_data[1]

        action, name, user, date = file_data

        # Check if the file is in the database
        if file_name not in current_file_database:

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
            file_history = current_file_database.get_file_history(name)

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

    return file_features, backup_meta_data

def vectorize(file_features, backup_meta_data):
    # Path length
    # Creation date?
    pass