import pickle
import sys

from tqdm.auto import tqdm

from src.loader.DataManager import DataManager
from src.loader.database.MongoDBConnector import MongoDBConnector, create_example_server
from src.od.FileServerModel import FileServerModel
from src.utils import Constants


def create_initial_model_and_store(db, data_manager, file_server):
    file_server_model = FileServerModel(file_server_id = file_server.id)
    file_server_model.initialize_model()
    received_data = file_server_model.fit(backup_data_collection = [
        data_manager.get_by_index(0),
        data_manager.get_by_index(1),
    ])

    data_manager.store_model_prediction(file_server.id, received_data)
    db.add_file_server_model(file_server_model.get_storable_components())


def continue_training_and_store(db, data_manager: DataManager, file_server, backup_index):
    # Load model data stored on mongo db
    server_id = file_server.id
    stored_file_server_model = db.get_file_server_model(server_id)
    file_server_model_id = stored_file_server_model.id if stored_file_server_model is not None else None

    # Create a file server and initialize it with the stored data
    file_server_model = FileServerModel(model_id = file_server_model_id, file_server_id = server_id)

    prev_backup_data = db.get_last_backup_metadata_by_file_server_id(file_server.id)
    file_server_model.initialize_model(stored_file_server_model, prev_backup_data)

    backup_metadata = data_manager.get_by_index(backup_index)

    model_prediction = file_server_model.predict(
        backup_data_collection = [backup_metadata],
        prev_backup_data = prev_backup_data,
        continues_training = True,
        ret_backup_features = True
    )
    data_manager.store_model_prediction(file_server.id, model_prediction)
    db.add_file_server_model(file_server_model.get_storable_components())


if __name__ == '__main__':
    Constants.verbose_printing = False

    _db = MongoDBConnector()
    if 'reset' in sys.argv:
        _db.reset_data()
        create_example_server(_db)
    _file_server = _db.get_file_server_by_name(name = Constants.test_file_server_name)

    _data_manager = DataManager(_db)
    _data_manager.load_data_from_file(data_path = "../../src/git-test/data")

    create_initial_model_and_store(_db, _data_manager, _file_server)
    for idx in tqdm(range(2, len(_data_manager))):
        continue_training_and_store(
            db = _db,
            data_manager = _data_manager,
            file_server = _file_server,
            backup_index = 2
        )
