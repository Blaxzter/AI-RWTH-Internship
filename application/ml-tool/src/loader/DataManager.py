import os

from tqdm.auto import tqdm
from src.utils.Constants import data_amount_per_line


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

                self.data[file] = list(
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

        file_data = []

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
        backup_data = self.sorted_key_list[idx]
        return backup_data, self.data[backup_data]

    def get_value_by_index(self, idx):
        backup_data = self.sorted_key_list[idx]
        return self.data[backup_data]

    def iterate_from(self, idx = 0):
        for backup_date in self.sorted_key_list[idx:]:
            yield backup_date, self.data[backup_date]

    def report_result(self, result):
        pass

    def get_data(self):
        return self.data.items()

    def get_data_values_as_list(self):
        return list(self.data.values())
