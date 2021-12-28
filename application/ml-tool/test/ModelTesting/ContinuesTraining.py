import pickle

from tqdm.auto import tqdm

from src.loader.DataManager import DataManager
from src.loader.database.MongoDBConnector import MongoDBConnector, create_example_server
from src.od.FileServerModel import FileServerModel
from src.utils import Constants

if __name__ == '__main__':
    db = MongoDBConnector()
    db.reset_data()
    create_example_server(db)
    file_server = db.get_file_server_by_name(name = Constants.test_file_server_name)

    data_manager = DataManager(db)
    data_manager.load_data_from_file(data_path = "../../src/git-test/data")

    server_id = file_server.id
    stored_file_server_model = db.get_file_server_model(server_id)

    file_server_model = FileServerModel(server_id, use_path_features = False)
    file_server_model.initialize_model(stored_file_server_model)
    received_data = file_server_model.fit(backup_data_list = [
        data_manager.get_value_by_index(0),
        data_manager.get_value_by_index(1),
    ])
    metadata_model_data = list(map(lambda x: dict(backup_metadata = x), received_data['meta_data_model']))

    data_iterator, data_amount = data_manager.get_iterator(start = 2)
    for backup_date, backed_up_files in tqdm(data_iterator, total = data_amount):
        backup_data = dict(
            date = backup_date,
            backup_data = backed_up_files,
            prev_backup_data = metadata_model_data[-1]['backup_metadata']
        )
        model_predict = file_server_model.predict(backup_data, continues_training = True, ret_backup_features = True)
        metadata_model_data.append(model_predict['meta_data_model'])

    metadata_model_prediction = list(
        map(lambda x: None if 'prediction' not in x else x['prediction'], metadata_model_data)
    )
    data_features = list(map(lambda x: x['backup_metadata']['feature'], metadata_model_data))
    features = list(data_features[0].keys())

    with open('../Visualization/data_features.pickle', 'wb') as handle:
        pickle.dump(data_features, handle, protocol = pickle.HIGHEST_PROTOCOL)
    with open('../Visualization/metadata_model_prediction.pickle', 'wb') as handle:
        pickle.dump(metadata_model_prediction, handle, protocol = pickle.HIGHEST_PROTOCOL)
    with open('../Visualization/features.pickle', 'wb') as handle:
        pickle.dump(features, handle, protocol = pickle.HIGHEST_PROTOCOL)
