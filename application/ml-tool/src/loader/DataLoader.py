#%%

import os

from dateutil.parser import parse
import time
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import numpy as np

from sklearn import preprocessing
from src.od.ODModel import OutlierDetectionModel

unix_date_scaler = preprocessing.MinMaxScaler()

#%%

_action_index = 0
_name_index = 1
_user_index = 2
_date_index = 3
_test_file_server_name = 'test_file_server'
_data_amount_per_line = 4

#%%
# Load data
data = {}

data_path = '../git-test/data'
for file in tqdm(os.listdir(data_path)):
    with open(f'{data_path}/{file}', 'r') as f:
        def preprocess(line):
            line = line.replace('\n', '')
            return line.split(',')
        data[file] = list(
            filter(
                lambda split_line: len(split_line) == _data_amount_per_line,
                map(preprocess, f.readlines())
            )
        )

#%%

len(data)

#%%

data_amount = list(map(lambda kv: (kv[0], len(kv[1])), data.items()))
" ".join(list(map(str, data_amount)))

#%%

labels, counts = zip(*data_amount)
plt.bar(labels, counts)

#%%

for k in sorted(data.keys())[:2]:
    print(data[k])

#%%

from src.loader.database.MongoDBConnector import MongoDBConnector, create_example_server

db = MongoDBConnector()
db.reset_data()
create_example_server(db)

#%%

from src.loader.FileDatabase import FileDatabase


def get_backup_meta_data(backed_up_files):
    backed_up_amount = len(backed_up_files)

    # Get the actions and counts of each action
    action_list = list(map(lambda d: d[_action_index], backed_up_files))
    uniques, counts = np.unique(action_list, return_counts = True)

    # Get the mean and std deviation of the min max scaled date range of all changes
    parse_access_dates = list(map(lambda d: parse(d[_date_index]), backed_up_files))
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
        uniques_counts = (uniques.tolist(), counts.tolist()),
        date_range = (earliest_date.item(), latest_date.item()),
        date_mean_std = (unix_dates_mean, unix_dates_std)
    )

# get_backup_meta_data(data['20180926-095306'])

file_database = []

def calc_moving_avg(old_avg, new_value, count):
    return old_avg * (count - 1) / count + new_value * count

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

# Go over each backup and do the schmu for every data
def load_file_server_model(file_server):
    file_server_id = file_server['_id']
    stored_model = db.get_file_server_model(file_server_id)
    model = OutlierDetectionModel(
        file_server = file_server,
        db_con = db,
        model = stored_model,
    )
    return model


def report_result(result):
    pass


def get_file_database(file_server, db):
    as_list = db.get_file_data_as_list(file_server['_id'])
    return as_list


def store_file_features(file_features, backup_meta_data, current_file_server):
    current_file_server_id = current_file_server['_id']

    added_meta_data = db.add_backup_meta_data(
        file_server_id = current_file_server_id,
        meta_data = backup_meta_data,
    )
    backup_data_id = added_meta_data.inserted_id

    db.add_file_data(
        file_server_id = current_file_server_id,
        backup_data_id = backup_data_id,
        file_data_list = file_features
    )


for backup_date in tqdm(sorted(data.keys())):
    backed_up_files = data[backup_date]

    current_file_server = db.get_file_server_by_name(_test_file_server_name)

    file_database = get_file_database(current_file_server, db)

    file_features, backup_meta_data = parse_feature_data(backed_up_files, file_database)
    vectorization = vectorize(file_features, backup_meta_data)

    store_file_features(file_features, backup_meta_data, current_file_server)

    # Model specific data
    model = load_file_server_model(file_server = current_file_server)
    result = model.outlier_detection(vectorization)
    model.fit_on_new_data(vectorization)
    model.update_db_model()

    report_result(result)

#%%

