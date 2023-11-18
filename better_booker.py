from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from scraper.scraper import Whitechapel_Scraper
from slot.slot import BookingSlot

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)


booking_page_scraper = Whitechapel_Scraper(driver)
booking_slots = booking_page_scraper.scrape('2023-11-24')

driver.quit()
