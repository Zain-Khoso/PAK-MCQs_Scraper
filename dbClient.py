# dbClient.py - Holds the Database class that inserts th given data on Atlas Cluster.

# Imports
from environs import Env
from pymongo.mongo_client import MongoClient


class Database:
    def __init__(self) -> None:
        self.ENV = Env()
        self.ENV.read_env()

        connection_string = self.ENV.str("atlas_connection_string")
        db_name = self.ENV.str("db_name")

        client = MongoClient(connection_string)

        self.DB = client[db_name]

    def insert_collection(self, collection_name: str, DATA: list) -> None:
        COLLECTION = self.DB[collection_name]
        COLLECTION.insert_many(DATA)
