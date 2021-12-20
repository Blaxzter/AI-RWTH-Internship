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
    data_manager.load_data_from_file()

    stored_file_server_model = db.get_file_server_model(file_server.id)

    file_server_model = FileServerModel()
    file_server_model.initialize_model(stored_file_server_model)
    file_server_model.fit(backup_data_list = [data_manager.get_value_by_index(0)])

    for backup_date, backed_up_files in tqdm(data_manager.iterate_from(1)):
        ret_data = file_server_model.predict(backed_up_files, continues_training = True, ret_backup_features = True)
