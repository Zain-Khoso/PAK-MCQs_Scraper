# scrper.py - Holds the Scraper class which scrapes questions from PAK-MCQS.

import re, requests as req
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError


class Scraper:
    def __init__(self) -> None:
        # Starting Page URL.
        self.current_url = "https://pakmcqs.com/category/software-engineering-mcqs/basics-of-software-engineering"

        # State of the scraper.
        self.running = True

        # List for storing Questions.
        self.DATA: list = []

    def getNextURL(self):
        # Selecting the next btn
        nextBtn = self.DOM.select_one("a.next")

        # Getting the next chapter URL.
        if nextBtn == None:
            self.running = False
        else:
            self.current_url = nextBtn.get("href")

    # The manager method
    def scrape(self):
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

                self.getQuestions()

            # Weither an error occurs or not.
            finally:
                self.getNextURL()

        return self.DATA

    # Method to get all questions from the current page.
    def getQuestions(self):
        """
        All the Questions with their options are stored in article tags,
        So selecting those tags from the DOM.
        """
        article_nodes = self.DOM.select("article")

        for article_node in article_nodes:
            # Dictionary to store the current question.
            QUESTION: dict = {}

            # Getting the question text. And storing it inside the QUESTION dict.
            QUESTION_TEXT: str = article_node.select_one('a[rel="bookmark"]').text
            QUESTION.setdefault("question", QUESTION_TEXT)

            # Getting the correct option text. And storing it inside the QUESTION dict.
            ANSWER_TEXT: str = article_node.select_one(
                "div.entry-content > p > strong"
            ).text
            if ANSWER_TEXT[-1] == "”":
                ANSWER_TEXT = ANSWER_TEXT[:-1]
            QUESTION.setdefault("answer", ANSWER_TEXT)

            # Getting the options. And storing them inside the QUESTION dict.
            options_text = article_node.select_one("div.entry-content > p").text
            OPTIONS: list = self.get_options(options_text)
            QUESTION.setdefault("options", OPTIONS)

            self.DATA.append(QUESTION)

    # Method to parse through the options.
    def get_options(self, text):
        # A Constant to store all the options
        OPTIONS: list = []

        # This is the regex which parses through the options text.
        regex = re.compile(
            r"""
                (A\. .*)                # Option: 1
                (\n)                    # New-Line
                (B\. .*)                # Option: 2
                (\n)                    # New-Line
                (C\. .*)                # Option: 3
                (\n)                    # New-Line
                (D\. .*)                # Option: 4
                (\n?)                   # New-Line
            """,
            re.VERBOSE,
        )

        # Parsing through the options text.
        parsed_options = regex.search(text)

        # Appending the options to the OPTIONS Constant.
        OPTIONS.append(parsed_options.group(1))
        OPTIONS.append(parsed_options.group(3))
        OPTIONS.append(parsed_options.group(5))
        OPTIONS.append(parsed_options.group(7))

        for index, option in enumerate(OPTIONS):
            if option[-1] == "”":
                OPTIONS[index] = option[:-1]

        return OPTIONS
