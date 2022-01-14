from matplotlib import pyplot as plt
from tqdm.auto import tqdm

from src.Exceptions import ODModelExists
from src.loader.database.MongoDBConnector import MongoDBConnector
from src.loader.database.dbmodels.IFileServerModel import IFileServerModel
from src.od.PathOcsvm import PathOCSVM
from src.utils.Constants import test_file_server_name
from test.TestUtils import create_path_sets

if __name__ == '__main__':
    db = MongoDBConnector()
    file_server = db.get_file_server_by_name(name = test_file_server_name)
    path_sets = create_path_sets(trim_data = -1, path = "../../src/git-test/data")

    train_set_percentage = 0.6

    train_sets = path_sets[:int(train_set_percentage * len(path_sets))]
    test_sets = path_sets[int((1 - train_set_percentage) * len(path_sets)):]

    file_server_model = db.get_file_server_model(file_server.id)

    path_ocsvm = PathOCSVM(path_sets = train_sets)
    if file_server_model is None:
        path_ocsvm.fit()
        file_server_model = IFileServerModel(file_server = file_server.id, path_ocsvm = path_ocsvm.get_stored_model())
        try:
            db.add_file_server_model(file_server_model)
        except ODModelExists:
            db.update_file_server_model(file_server_model)
    else:
        path_ocsvm.load_stored_model(file_server_model)

    res = []
    for i, test_set in tqdm(enumerate(test_sets), desc = "Test Path:", total = len(test_sets)):
        res.append(path_ocsvm.predict([test_set]))

    plt.bar(list(range(len(res))), list(map(lambda x: x.item(), res)))
    plt.show()
