# scrper.py - Holds the Scraper class which scrapes questions from PAK-MCQS.

import re, requests as req
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError


class Scraper:
    def __init__(self, startURL: str) -> None:
        # URL of the page on which scraper is scraping.
        self.current_url = startURL

        # Creating the initial DOM.
        res = req.get(self.current_url)
        res.raise_for_status()
        self.DOM = BeautifulSoup(res.text, "html.parser")

        # State of the scraper.
        self.running = True

        # List for storing Questions.
        self.DATA: list = []

    # Method to get the next page's URL.
    def getNextURL(self) -> None:
        # Selecting the next btn
        nextBtn = self.DOM.select_one("a.next")

        # Getting the next chapter URL.
        if nextBtn == None:
            self.running = False
        else:
            self.current_url = nextBtn.get("href")

    # The manager method
    def scrape(self) -> list:
        # Looping through all the pages.
        while self.running:
            # Downloading the page DOM.
            try:
                res = req.get(self.current_url)
                res.raise_for_status()

            # Handeling Connection or HTTPError.
            except (ConnectionError, HTTPError) as err:
                print("Error: %s" % err)

            # If there was no Exception.
            else:
                # Creating DOM.
                self.DOM = BeautifulSoup(res.text, "html.parser")

                # TODO:
                # print(f"Started Parsing: {self.current_url}")

                self.getQuestions()

            # Weither an error occurs or not.
            finally:
                self.getNextURL()

        return self.DATA

    # Method to get all questions from the current page.
    def getQuestions(self) -> None:
        """
        All the Questions with their options are stored in article tags,
        So selecting those tags from the DOM.
        """
        article_nodes = self.DOM.select("article")

        for index, article_node in enumerate(article_nodes):
            # Dictionary to store the current question.
            QUESTION: dict = {}

            # Trying to get the raw data from the DOM.
            try:
                QUESTION_TEXT: str = article_node.select_one('a[rel="bookmark"]').text
                ANSWER_TEXT: str = article_node.select_one(
                    "div.entry-content > p > strong"
                ).text
                options_text = article_node.select_one("div.entry-content > p").text
                OPTIONS: list = self.get_options(options_text)

            # If something goes wrong then skipping this question.
            except:
                continue

            # Other wise formating the data and appending it the this questions dict.
            else:
                QUESTION.setdefault("question", QUESTION_TEXT)
                if ANSWER_TEXT[-1] == "”":
                    ANSWER_TEXT = ANSWER_TEXT[:-1]
                QUESTION.setdefault("answer", ANSWER_TEXT)
                QUESTION.setdefault("options", OPTIONS)

            self.DATA.append(QUESTION)

    # Method to parse through the options.
    def get_options(self, text) -> list:
        # A Constant to store all the options
        OPTIONS: list = []

        # This is the regex which parses through the options text.
        regex = re.compile(
            r"""
                (\s?)(A\.? .*)                  # Option: 1
                (\s?)(\n)                       # New-Line
                (\s?)(B\.? .*)                  # Option: 2
                (\s?)(\n)                       # New-Line
                (\s?)(C\.? .*)                  # Option: 3
                (\s?)(\n)                       # New-Line
                (\s?)(D\.? .*)                  # Option: 4
                (\s?)(\n?)                      # New-Line
            """,
            re.VERBOSE,
        )

        # Parsing through the options text.
        parsed_options = regex.search(text)

        # Appending the options to the OPTIONS Constant.
        OPTIONS.append(parsed_options.group(2))
        OPTIONS.append(parsed_options.group(6))
        OPTIONS.append(parsed_options.group(10))
        OPTIONS.append(parsed_options.group(14))

        for index, option in enumerate(OPTIONS):
            if option[-1] == "”":
                OPTIONS[index] = option[:-1]

        return OPTIONS
