# app.py - __main__ file of this Scraper.

# Imports
import requests, threading, re
from scraper import Scraper
from dbClient import Database
from bs4 import BeautifulSoup


# main Function where the whole program's execution takes place.
def main():
    # URL of the home of PAK-MCQs.
    HOME_URL: str = "https://pakmcqs.com/"

    MCQS_CATEGORIES_URLs: list = get_all_available_mcqs_categories(HOME_URL)

    THREADS: list = []

    for URL in MCQS_CATEGORIES_URLs:
        thread = threading.Thread(target=download_and_insert, args=(URL,))
        THREADS.append(thread)
        thread.start()

    for thread in THREADS:
        thread.join()

    print("\n\nCompleted")


# This function will be managing each thread which is created by main function.
def download_and_insert(URL):
    # Find the index of last '/' cuz after the the name comes.
    last_index = URL.rfind("/")

    MCQ_type_name = URL[last_index + 1 :]

    print("Start Scraper For: %s" % URL)

    # Instancing the Scraper class & then running the scraper.
    BOT: Scraper = Scraper(URL)
    DATA: list = BOT.scrape()

    # Inserting the current questions data to the Database.
    DB = Database()
    DB.insert_collection(MCQ_type_name, DATA)

    print("Ended Scraper For: %s" % URL)


# Function scrapes the home_page to get the urls of all the available MCQs categories.
def get_all_available_mcqs_categories(home_page_url: str):
    # Names of categories which don't contain MCQs.
    useless_menu_names = [
        "SUBMIT MCQS",
        "Follow us on Facebook!",
        "PAKMCQS QUIZ",
        "Top Contributors",
        "INFO",
        "POPULAR CATEGORIES",
        "Online Quiz",
    ]

    # List to store the URLS
    MCQS_CATEGORIES: list = []

    # Downloading the homepage for parsing.
    response = requests.get(home_page_url)
    response.raise_for_status()

    # Creating a DOM from this downloaded HTML file.
    DOM = BeautifulSoup(response.text, "html.parser")

    # Selecting all the Menus of MCQs available.
    menus = DOM.select("aside.widget_nav_menu")

    # These for loops get all the URLs which are present in URL menus.
    for menu in menus:
        menu_heading = menu.select_one("h1.widget-title")

        if menu_heading.text in useless_menu_names:
            continue

        categories = menu.select("li.menu-item > a")

        for category in categories:
            MCQS_CATEGORIES.append(category.get("href"))

    return MCQS_CATEGORIES


# Using this condition here as a best practice to run python scripts.
if __name__ == "__main__":
    main()
