import pickle
from collections import defaultdict

from tqdm.auto import tqdm

from src.loader.DataManager import DataManager
from src.loader.database.MongoDBConnector import MongoDBConnector, create_example_server
from src.od.FileServerModel import FileServerModel
from src.utils import Constants

if __name__ == '__main__':
    Constants.verbose_printing = False

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

    re_predict = file_server_model.re_predict()
    re_predict_data = defaultdict(list)
    for model_name, model_data in re_predict.items():
        re_predict_data[model_name].append(model_data)

    model_ret_data = defaultdict(list)
    for model_name, model_data in received_data.items():
        for model_rets in model_data:
            model_ret_data[model_name].append(model_rets)

    data_iterator, data_amount = data_manager.get_iterator(start = 2)
    for backup_date, backed_up_files in tqdm(data_iterator, total = data_amount):
        backup_data = [dict(
            backup_date = backup_date,
            backup_data = backed_up_files,
        )]
        prev_backup_data = None
        if file_server_model.use_meta_data_features:
            prev_backup_data = model_ret_data['meta_data_model'][-1]['backup_metadata']

        model_predict = file_server_model.predict(
            backup_data_collection = backup_data,
            prev_backup_data = prev_backup_data,
            continues_training = True,
            ret_backup_features = True
        )

        re_predict = file_server_model.re_predict()

        for model_name, model_data in model_predict.items():
            for model_rets in model_data:
                model_ret_data[model_name].append(model_rets)

        for model_name, model_data in re_predict.items():
            re_predict_data[model_name].append(model_data)

    with open('../Visualization/re_predict_data.pickle', 'wb') as handle:
        pickle.dump(re_predict_data, handle, protocol = pickle.HIGHEST_PROTOCOL)
