from tqdm.auto import tqdm

from src.loader.DataManager import DataManager
from src.loader.database.MongoDBConnector import MongoDBConnector, create_example_server
from src.od.ODModel import OutlierDetectionModel
from src.od.Preprocessor import parse_feature_data, vectorize
from src.utils.Constants import test_file_server_name

if __name__ == '__main__':

    db = MongoDBConnector()
    db.reset_data()
    create_example_server(db)

    data_manager = DataManager(db)
    data_manager.load_data_from_file()

    for backup_date, backed_up_files in tqdm(data_manager.getData()):


        file_features, backup_meta_data = parse_feature_data(backed_up_files, file_database)
        vectorization = vectorize(file_features, backup_meta_data)

        data_manager.store_file_features(file_features, backup_meta_data, current_file_server)

        # Model specific data
        model = OutlierDetectionModel.load_file_server_model(db = db, file_server = current_file_server)
        result = model.outlier_detection(vectorization)
        model.fit_on_new_data(vectorization)
        model.update_db_model()

        data_manager.report_result(result)
