from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import datetime
from slot.slot import BookingSlot


class Scraper:
    def scrape(self):
        pass


class Whitechapel_Scraper(Scraper):

    def __init__(self, driver: webdriver) -> None:
        self.driver = driver
        self.home_page = 'https://bookings.better.org.uk'
        super().__init__()

    def scrape(self, date_as_yyyy_mm_dd):
        try:
            url = f'{self.home_page}/location/whitechapel-sports-centre/badminton-60min/{date_as_yyyy_mm_dd}/by-time'
            self.driver.get(url)
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'ClassCardComponent__ClassTime-sc-1v7d176-3')))

            log_in_result = self.handle_log_in()
            print(f'Log in success: {log_in_result}')
            if not log_in_result:
                return None

            self.page_source = self.driver.page_source

            return self.handle_html_parsing_and_return_slots()

        except TimeoutException:
            print('Date not available yet!')
            return None
        return

    def handle_log_in(self):

        try:
            authenticated_box = self.driver.find_element(By.CLASS_NAME,
                                                         'AuthButtonComponent__DesktopButton-sc-1evy10l-0')
        except NoSuchElementException:
            print('Not logged in')

            pre_login_button = self.driver.find_element(By.CLASS_NAME,
                                                        'Button__StyledButton-sc-5h7i9w-1')
            pre_login_button.click()

            username_field = self.driver.find_element(By.CLASS_NAME,
                                                      'SharedLoginComponent__EmailInput-sc-hdtxi2-2')
            password_field = self.driver.find_element(By.CLASS_NAME,
                                                      'PasswordInput__StyledFormControl-sc-m5owcc-1')

            # Enter login credentials
            username_field.send_keys('zayyt111@gmail.com')
            password_field.send_keys('Zayyartun123!')

            # Find and click the login button
            login_button = self.driver.find_element(By.CSS_SELECTOR,
                                                    '.Button__StyledButton-sc-5h7i9w-1.ccoZFi.SharedLoginComponent__LoginButton-sc-hdtxi2-5.iHMekP')
            print(login_button.text)
            login_button.click()

            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'AuthButtonComponent__DesktopButton-sc-1evy10l-0')))
            authenticated_box = self.driver.find_element(By.CLASS_NAME,
                                                         'AuthButtonComponent__DesktopButton-sc-1evy10l-0')

            if authenticated_box.text == "My account":
                return True
        except:
            return False
        return False

    def handle_html_parsing_and_return_slots(self):
        soup = BeautifulSoup(self.page_source, 'html.parser')
        time_slots = soup.find_all(
            class_='ClassCardComponent__ClassTime-sc-1v7d176-3')
        availabilities = soup.find_all(
            class_='ContextualComponent__BookWrap-sc-eu3gk6-1')
        book_links_raw = soup.find_all(
            class_='ContextualComponent__BookButton-sc-eu3gk6-2')
        book_links = [div_element.find('a')['href']
                      for div_element in book_links_raw]
        all_info = zip(time_slots, availabilities, book_links)
        _ = [print(f'Time: {time.text}, Availabilities: {availabilities.text[:-4]}, Book link: {self.home_page}{book_link}')
             for time, availabilities, book_link in all_info]
        booking_slots = [BookingSlot(time, availabilities, book_link)
                         for time, availabilities, book_link in all_info]
        return booking_slots
