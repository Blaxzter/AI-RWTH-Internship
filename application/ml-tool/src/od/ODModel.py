from src.utils.Utils import get_random_string


class OutlierDetectionModel:

    def __init__(self, file_server, db_con, model = None):
        self.file_server = file_server
        self.db_con = db_con

        if model:
            print("Create model from stored data")

    def outlier_detection(self, vectorization):
        pass

    def fit_on_new_data(self, vectorization):
        pass

    def update_db_model(self):

        serialized_model = get_random_string()

        self.db_con.update_file_server_model(
            file_server_id = self.file_server['_id'],
            model = serialized_model,
        )

