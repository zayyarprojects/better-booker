from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import datetime


class Scraper:
    def scrape(self):
        pass


class Whitechapel_Scraper(Scraper):

    def __init__(self, driver: webdriver) -> None:
        self.driver = driver
        super().__init__()

    def scrape(self):
        try:
            home_page = 'https://bookings.better.org.uk'
            url = f'{home_page}/location/whitechapel-sports-centre/badminton-60min/2023-10-26/by-time'
            self.driver.get(url)
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'ClassCardComponent__ClassTime-sc-1v7d176-3')))
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            time_slots = soup.find_all(
                class_='ClassCardComponent__ClassTime-sc-1v7d176-3')
            availabilities = soup.find_all(
                class_='ContextualComponent__BookWrap-sc-eu3gk6-1')
            book_links_raw = soup.find_all(
                class_='ContextualComponent__BookButton-sc-eu3gk6-2')
            book_links = [div_element.find('a')['href']
                          for div_element in book_links_raw]
            all_info = zip(time_slots, availabilities, book_links)
            _ = [print(f'Time: {time.text}, Availabilities: {availabilities.text[:-4]}, Book link: {home_page}{book_link}')
                 for time, availabilities, book_link in all_info]
        except TimeoutException:
            print('Date not available yet!')
        return
