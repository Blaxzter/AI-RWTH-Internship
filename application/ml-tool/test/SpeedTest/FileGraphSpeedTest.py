import time

from tqdm import tqdm

from src.od.searchutils.FileTreeDatabase import FileTreeDatabase
from src.utils import Constants
from test.TestUtils import load_data

if __name__ == '__main__':
    backup_data = load_data(trim_data = -1, path = "../../src/git-test/data")

    # start = time.time()
    # print("Start")
    #
    # full_set = []
    #
    # counter = 0
    # prev_stored = 0
    #
    # backup_data_list = backup_data.get_data_values_as_list()
    #
    # comp_path_set = list(map(lambda feature: feature[Constants.name_index], backup_data_list[0]))
    # for backup_list in tqdm(backup_data_list[1:]):
    #     path_set = list(map(lambda feature: feature[Constants.name_index], backup_list))
    #     for path in path_set:
    #         if path in comp_path_set:
    #             counter += 1
    #
    #         if path not in full_set:
    #             full_set.append(path)
    #             prev_stored += 1
    #
    #     comp_path_set = path_set
    #
    # end = time.time()
    # print(f'counter: {counter} prev_stored: {prev_stored} time: {end - start}')

    start = time.time()
    print("Start")

    full_graph = FileTreeDatabase()

    counter = 0
    prev_stored = 0

    backup_data_list = backup_data.get_data_values_as_list()

    comp_path_set = FileTreeDatabase(backup_data_list[0])
    for backup_set in tqdm(backup_data_list[1:]):
        path_list = list(map(lambda feature: feature[Constants.name_index], backup_set))
        for path in path_list:
            if path in comp_path_set:
                counter += 1

            if path not in full_graph:
                full_graph.add_backup_instance(path)
                prev_stored += 1

        comp_path_set = FileTreeDatabase(path_list = path_list)

    end = time.time()
    print(f'counter: {counter} prev_stored: {prev_stored} time: {end - start}')
