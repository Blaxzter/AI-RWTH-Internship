from collections import defaultdict


class FileDatabase:

    def __init__(self, file_data_list, is_sorted = False):
        self.file_data_list = file_data_list

        self.file_data_by_name = defaultdict(list)

        self.file_names = []

        for file_data in file_data_list:
            file_name = file_data['name']
            self.file_names.append(file_name)
            self.file_data_by_name[file_name].append(file_data)

        if is_sorted:
            for key, value in self.file_data_by_name.items():
                self.file_data_by_name[key] = list(sorted(value, key = lambda d: d['action_date']))

    def __contains__(self, item):
        return item in self.file_names

    def get_file_history(self, name):
        return self.file_data_by_name[name]
