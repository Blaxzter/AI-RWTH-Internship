from src.loader.database.MongoDBConnector import MongoDBConnector, create_example_server

if __name__ == '__main__':
    _db = MongoDBConnector()

    for i in range(10):
        create_example_server(_db, i)