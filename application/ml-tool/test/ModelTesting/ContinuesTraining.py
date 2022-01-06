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

    file_server_model = FileServerModel(server_id)
    file_server_model.initialize_model(None)
    received_data = file_server_model.fit(backup_data_collection = [
        data_manager.get_by_index(0),
        data_manager.get_by_index(1),
    ])

    model_ret_data = {model_name: [] for model_name in file_server_model.get_used_models()}
    for model_name, model_data in received_data.items():
        for model_rets in model_data:
            model_ret_data[model_name].append(model_rets)

    data_iterator, data_amount = data_manager.get_iterator(start = 2)
    for backup_date, backed_up_files in tqdm(data_iterator, total = data_amount):
        backup_data = dict(
            backup_date = [backup_date],
            backup_data = [backed_up_files],
        )
        if file_server_model.use_meta_data_features:
            backup_data['prev_backup_data'] = model_ret_data['meta_data_model'][-1]['backup_metadata']

        model_predict = file_server_model.predict(backup_data, continues_training = True, ret_backup_features = True)

        for model_name, model_data in model_predict.items():
            for model_rets in model_data:
                model_ret_data[model_name].append(model_rets)

    model_predictions = {
        model_name: list(
            map(lambda x: None if 'prediction' not in x else x['prediction'], model_data)
        ) for model_name, model_data in model_ret_data.items()
    }
    with open('../Visualization/prediction.pickle', 'wb') as handle:
        pickle.dump(model_predictions, handle, protocol = pickle.HIGHEST_PROTOCOL)

    if file_server_model.use_meta_data_features:
        data_features = list(map(
            lambda x: x[Constants.backup_metadata_dict_name][Constants.backup_features_dict_name],
            model_ret_data['meta_data_model']))
        features = list(data_features[0].keys())

        with open('../Visualization/data_features.pickle', 'wb') as handle:
            pickle.dump(data_features, handle, protocol = pickle.HIGHEST_PROTOCOL)

        with open('../Visualization/features.pickle', 'wb') as handle:
            pickle.dump(features, handle, protocol = pickle.HIGHEST_PROTOCOL)
