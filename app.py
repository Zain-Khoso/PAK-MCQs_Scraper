# Main file for this scraper.
# Imports
from scraper import Scraper
from environs import Env
from pymongo.mongo_client import MongoClient
from pprint import pprint


# Main Function where the whole program's execution takes place.
def main():
    # Call to Scrapper.
    BOT = Scraper()
    DATA: list = BOT.scrape()

    # TODO: Remove this comment to insert the data on the cluster.
    # database_inserter(DATA)


def database_inserter(DATA: dict):
    env = Env()
    env.read_env()

    username = env.str("atlas_username")
    password = env.str("atlas_password")

    client = MongoClient(
        f"mongodb+srv://{username}:{password}@maincluster.bwozlbo.mongodb.net/?retryWrites=true&w=majority"
    )

    DB = client["pak-mcqs"]
    COLLECTION = DB["software-engineering"]
    COLLECTION.insert_many(DATA)


# Using this condition here as a best practice to run python scripts.
if __name__ == "__main__":
    main()
