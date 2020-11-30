import selenium as se
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time

chromeOptions = se.webdriver.ChromeOptions()
# chromeOptions.add_argument("headless")
chromeOptions.add_argument("user-data-dir=selenium")

driver = webdriver.Chrome(
    r"C:\Users\kreat\Documents\GitHub\WhatsappDesktopPlusPlus-Python\Driver\chromedriver.exe", options=chromeOptions)

driver.get("http://web.whatsapp.com")

time.sleep(5)
html = driver.page_source

soup = bs(html, 'lxml')

if soup.find_all("div", {"class": "_3LtPa"}):
    print("Tag Found")

driver.quit
