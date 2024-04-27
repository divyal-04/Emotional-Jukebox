# youtube_scraper.py

import os
from selenium import webdriver
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchWindowException

class YoutubeBot:
    def __init__(self, driver_path=r"D:\T.E\SEM 6\Mini proj\122_scraper\chromedriver-win64\chromedriver.exe"):
        # Set Chromedriver path
        CHROMEDRIVER_PATH = driver_path

        # Set environment variable
        os.environ['PATH'] += ':' + CHROMEDRIVER_PATH

        # Create ChromeOptions
        option = webdriver.ChromeOptions()

        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument("--window-size=1920,1080")

        # List of user agents
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        ]

        # Select a random user agent
        userAgent = random.choice(user_agents)
        option.add_argument(f'--user-agent={userAgent}')

        self.driver = webdriver.Chrome(options=option)

    def open_youtube(self):
        url = "https://youtube.com/"
        self.driver.get(url)

    def search(self, query):
        search_box = self.driver.find_element(By.ID, 'search-form')
        search_input = search_box.find_element(By.TAG_NAME, 'input')
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)


def search_on_youtube(query):
    youtube_bot = YoutubeBot()  # Initialize YoutubeBot without any arguments
    try:
        youtube_bot.open_youtube()
        youtube_bot.search(query)  # Pass the query to the search method
    finally:
        pass

