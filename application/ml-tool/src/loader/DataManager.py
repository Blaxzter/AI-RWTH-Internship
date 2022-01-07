import os
from collections import defaultdict

from tqdm.auto import tqdm

from src.loader.database.dbmodels.IBackupMetaData import IBackupMetaData
from src.utils import Utils, Constants
from src.utils.Constants import data_amount_per_line


def get_first_element_by_key(backup_data_list, key):
    ret_value = None
    for backup_data in backup_data_list:
        if key in backup_data:
            ret_value = backup_data[key]
            break
        elif Constants.backup_metadata_dict_name in backup_data and key in backup_data[Constants.backup_metadata_dict_name]:
            ret_value = backup_data[Constants.backup_metadata_dict_name][key]
            break

    return ret_value


class DataManager:
    def __init__(self, db_con):
        self.data = {}
        self.db_con = db_con
        self.sorted_key_list = []

    def load_data_from_file(self, data_path = './git-test/data', trim_data = -1):
        # Load data
        listdir = os.listdir(data_path)

        if trim_data >= 0:
            listdir = listdir[:trim_data]

        for file in tqdm(listdir, desc = "Load files:"):
            with open(f'{data_path}/{file}', 'r') as f:
                def preprocess(line):
                    line = line.replace('\n', '')
                    return line.split(',')

                self.data[Utils.get_unix_time(file)] = list(
                    filter(
                        lambda split_line: len(split_line) == data_amount_per_line,
                        map(preprocess, f.readlines())
                    )
                )
        self.sorted_key_list = list(sorted(self.data.keys()))

    def store_file_features(self, file_features, backup_meta_data, current_file_server):
        current_file_server_id = current_file_server['_id']

        added_meta_data = self.db_con.add_backup_meta_data(
            file_server_id = current_file_server_id,
            meta_data = backup_meta_data,
        )
        backup_data_id = added_meta_data.inserted_id

        self.db_con.add_file_data(
            file_server_id = current_file_server_id,
            backup_data_id = backup_data_id,
            file_data_list = file_features
        )

    def __len__(self):
        return len(self.sorted_key_list)

    def __getitem__(self, index):
        """
        Get the data from the loaded data
        :param index: The key of the data
        :return:
        """
        return self.data[index]

    def __iter__(self):
        for backup_date in self.sorted_key_list:
            yield backup_date, self.data[backup_date]

    def get_by_index(self, idx):
        backup_date = self.sorted_key_list[idx]
        ret_dict = dict(
            backup_date = backup_date,
            backup_data = self.data[backup_date]
        )
        return ret_dict

    def iterate_from(self, start = None, end = None):
        idx = 0 if start is None else start
        end_idx = len(self.sorted_key_list) if end is None else end
        for backup_date in self.sorted_key_list[idx:end_idx]:
            yield backup_date, self.data[backup_date]

    def get_iterator(self, start = None, end = None):
        idx = 0 if start is None else start
        end_idx = len(self.sorted_key_list) if end is None else end
        return iter(
            [(backup_date, self.data[backup_date]) for backup_date in self.sorted_key_list[idx:end_idx]]), end_idx - idx

    def report_result(self, result):
        pass

    def get_data(self):
        return self.data.items()

    def get_data_values_as_list(self):
        return list(self.data.values())

    def store_model_prediction(self, file_server_id, model_prediction):

        grouped_by_backup_date = defaultdict(list)
        for model_name, model_data_per_backup in model_prediction.items():
            for data_of_date in model_data_per_backup:
                add_data = data_of_date
                add_data['model_name'] = model_name
                grouped_by_backup_date[data_of_date[Constants.backup_date_dict_name]].append(add_data)

        for backup_date, backup_data_list in grouped_by_backup_date.items():
            store_data = IBackupMetaData(
                backup_date = backup_date,
                predictions = {model_name: value for model_name, value in
                               map(lambda x: (x['model_name'], x[Constants.prediction_dict_name]),
                                   filter(lambda x: Constants.prediction_dict_name in x, backup_data_list))
                               },
                features = get_first_element_by_key(backup_data_list, Constants.backup_features_dict_name),
                action_data = get_first_element_by_key(backup_data_list, Constants.action_data_dict_name)
            )

            added_col = self.db_con.add_backup_meta_data(file_server_id, store_data)
            self.db_con.add_backup_meta_data_file_tree(
                added_col.inserted_id,
                get_first_element_by_key(backup_data_list, Constants.file_tree_dict_name)
            )
