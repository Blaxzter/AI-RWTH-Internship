import pickle

from src.loader.DataManager import DataManager
from src.loader.database.MongoDBConnector import MongoDBConnector
from src.od.FileServerModel import FileServerModel
from src.utils import Constants

if __name__ == '__main__':
    # Constants.verbose_printing = False

    data_manager = DataManager(None)
    data_manager.load_data_from_file(data_path = "../../src/git-test/data")

    file_server_model = FileServerModel(file_server_id = None, use_meta_data_features = False)
    file_server_model.initialize_model(None)
    received_data = file_server_model.fit(backup_data_collection = [
        dict(backup_date = backup_date, backup_data = backup_data) for backup_date, backup_data in data_manager
    ])

    model_predict = file_server_model.re_predict()

    print("finished")

    with open('../Visualization/one_prediction.pickle', 'wb') as handle:
        pickle.dump(model_predict, handle, protocol = pickle.HIGHEST_PROTOCOL)
