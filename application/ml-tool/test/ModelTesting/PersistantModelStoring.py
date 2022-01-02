import pickle
import sys

from tqdm.auto import tqdm

from src.loader.DataManager import DataManager
from src.loader.database.MongoDBConnector import MongoDBConnector, create_example_server
from src.od.FileServerModel import FileServerModel
from src.utils import Constants


def create_initial_model_and_store(db, data_manager, file_server):
    file_server_model = FileServerModel(file_server_id = file_server.id,
                                        model_id = None, use_path_features = False)
    file_server_model.initialize_model()
    received_data = file_server_model.fit(backup_data_collection = [
        data_manager.get_by_index(0),
        data_manager.get_by_index(1),
    ])
    db.store_backup_data(file_server.id, received_data['meta_data_model'])
    db.add_file_server_model(file_server_model.get_storable_components())


def continue_training_and_store(db, data_manager: DataManager, file_server, backup_index):
    server_id = file_server.id
    stored_file_server_model = db.get_file_server_model(server_id)
    file_server_model_id = stored_file_server_model.id if stored_file_server_model is not None else None

    file_server_model = FileServerModel(model_id = file_server_model_id, file_server_id = server_id,
                                        use_path_features = False)

    prev_backup_data = db.get_last_backup_metadata_by_file_server_id(file_server.id)
    file_server_model.initialize_model(stored_file_server_model, prev_backup_data)

    backup_metadata = data_manager.get_by_index(backup_index)
    backup_metadata[Constants.prev_backup_data_dict_name] = prev_backup_data

    model_predict = file_server_model.predict(backup_metadata, continues_training = True, ret_backup_features = True)
    db.store_backup_data(file_server.id, [model_predict['meta_data_model']])

if __name__ == '__main__':

    _db = MongoDBConnector()
    if 'reset' in sys.argv:
        _db.reset_data()
        create_example_server(_db)
    _file_server = _db.get_file_server_by_name(name = Constants.test_file_server_name)

    _data_manager = DataManager(_db)
    _data_manager.load_data_from_file(data_path = "../../src/git-test/data")

    create_initial_model_and_store(_db, _data_manager, _file_server)
    continue_training_and_store(_db, _data_manager, _file_server, 2)
