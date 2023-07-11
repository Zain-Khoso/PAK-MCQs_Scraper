# app.py - __main__ file of this Scraper.

# Imports
from scraper import Scraper
from dbClient import Database


# main Function where the whole program's execution takes place.
def main():
    # Instancing the Scraper class & then running the scraper.
    BOT: Scraper = Scraper(
        "https://pakmcqs.com/category/software-engineering-mcqs/basics-of-software-engineering"
    )
    DATA: list = BOT.scrape()

    # Inserting the current questions data to the Database.
    DB = Database()
    # TODO: Remove this comment to insert the data on the cluster.
    # DB.insert_collection("software-engineering", DATA)


# Using this condition here as a best practice to run python scripts.
if __name__ == "__main__":
    main()
