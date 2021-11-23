from src.loader.DataManager import DataManager


def create_path_lists(trim_data = -1, add_root = True):
    data_manager = DataManager(None)
    data_manager.load_data_from_file("../src/git-test/data")
    # %%
    from src.utils.Constants import name_index
    from tqdm import tqdm
    training_data = []
    if trim_data == -1:
        data = data_manager.getData()
    else:
        data = list(data_manager.getData())[:trim_data]
    for backup_date, backed_up_files in tqdm(data):
        for file in backed_up_files:
            path = file[name_index].lower().split('/')
            if add_root:
                path.insert(0, 'root')
            training_data.append(path)

    return training_data


def create_path_sets(trim_data = -1, add_root = True, path="../src/git-test/data"):
    data_manager = DataManager(None)
    data_manager.load_data_from_file(path)
    # %%
    from src.utils.Constants import name_index
    from tqdm import tqdm
    training_data = []
    if trim_data == -1:
        data = data_manager.getData()
    else:
        data = list(data_manager.getData())[:trim_data]
    for backup_date, backed_up_files in tqdm(data, desc = "Convert to Path-Set:"):
        n_set = []
        for file in backed_up_files:
            path = file[name_index].lower().split('/')
            if add_root:
                path.insert(0, 'root')
            n_set.append(path)
        training_data.append(n_set)

    return training_data

def get_path_indexed_path_element(path_list, element_idx = -1):
    vocabulary = []
    for path in path_list:
        if len(path) < abs(element_idx):
            continue

        indexed_element = path[element_idx]
        if indexed_element not in vocabulary:
            vocabulary.append(indexed_element)
    return vocabulary


if __name__ == '__main__':
    path_lists = create_path_lists(trim_data = 10)
    folder_vocab = get_path_indexed_path_element(path_lists, element_idx = -2)
    print(folder_vocab)
