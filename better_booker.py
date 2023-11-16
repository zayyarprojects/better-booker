from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from scraper.scraper import Whitechapel_Scraper

options = Options()
options.headless = True

driver = webdriver.Chrome(ChromeDriverManager(
    "2.26").install(), options=options)

booking_page_scraper = Whitechapel_Scraper(driver)
booking_page_scraper.scrape()
