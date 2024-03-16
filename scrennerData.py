import requests
from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import codecs
import re

# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# from webdriver_manager.chrome import ChromeDriverManager


# driver=webdriver.Chrome(service=Service(ChromeDriverManager(version='114.0.5735.90').install()))

# driver = webdriver.Firefox(executable_path='home/vboxuser/Downloads/geckodriver.exe')




# driver = webdriver.Firefox()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))



#balance-sheet
#profit-loss
#shareholding

val = 'https://www.screener.in/company/PAYTM/'

# r = requests.get(url)

wait = WebDriverWait(driver, 10)
driver.get(val)

element = driver.find_element(By.XPATH, "//section[@id='shareholding']/div[2]")

print(element.text)



