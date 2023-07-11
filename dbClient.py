# dbClient.py - Holds the Database class that inserts th given data on Atlas Cluster.

# Imports
from environs import Env
from pymongo.mongo_client import MongoClient


class Database:
    def __init__(self) -> None:
        self.ENV = Env()
        self.ENV.read_env()

        username = self.ENV.str("atlas_username")
        password = self.ENV.str("atlas_password")

        client = MongoClient(
            f"mongodb+srv://{username}:{password}@maincluster.bwozlbo.mongodb.net/?retryWrites=true&w=majority"
        )

        self.DB = client["pak-mcqs"]

    def insert_collection(self, collection_name: str, DATA: list) -> None:
        COLLECTION = self.DB[collection_name]
        COLLECTION.insert_many(DATA)
