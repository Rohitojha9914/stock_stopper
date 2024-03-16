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
import time
import psycopg2
import pandas as pd

# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

# from webdriver_manager.chrome import ChromeDriverManager


# driver=webdriver.Chrome(service=Service(ChromeDriverManager(version='114.0.5735.90').install()))

# driver = webdriver.Firefox(executable_path='home/vboxuser/Downloads/geckodriver.exe')




# # driver = webdriver.Firefox()
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))



# # #balance-sheet
# # #profit-loss
# # #shareholding

# val = 'https://www.nseindia.com/get-quotes/equity?symbol=TCS'

# # r = requests.get(url)

# # wait = WebDriverWait(driver, 10)
# # driver.implicitly_wait(10)
# driver.get(val)

# # element = driver.find_element(By.XPATH, "//div[@id='info-tradeinfo']//div[@class='tbl_leftcol_fix tbl_tradeinfo']")

# # driver.implicitly_wait(14)


# time.sleep(2)

# sector = driver.find_element(By.XPATH, "//div[@id='info-tradeinfo']//div[@class=' mt-1 py-1 security-spcaing']//div[@class='row']/div[1]")

# element = driver.find_element(By.XPATH, "//div[@id='info-tradeinfo']//div[@class='tbl_leftcol_fix tbl_tradeinfo']")


# print(sector.text)
# print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
# print(element.text)


def insert_listedcompany():

    
    conn = None
    conn = psycopg2.connect( database="stock", user='rohit', password='1234', host='localhost', port= '5432')
    cursor = conn.cursor()
    postgreSQL_select_Query = "select * from listedcompany"
    cursor.execute(postgreSQL_select_Query)
    data = cursor.fetchall()
    # print(len(list(data)))
    

    for index in range(0,len(list(data))):

        try: 
            stock_name= str(data[index][2])

            time.sleep(1)

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            
            val = "https://www.nseindia.com/get-quotes/equity?symbol={0}".format(stock_name)
            
            print(val)

            driver.get(val)

            time.sleep(2)

            sector = driver.find_element(By.XPATH, "//div[@id='info-tradeinfo']//div[@class=' mt-1 py-1 security-spcaing']//div[@class='row']/div[1]")

            element = driver.find_element(By.XPATH, "//div[@id='info-tradeinfo']//div[@class='tbl_leftcol_fix tbl_tradeinfo']")

            # //div[@id='info-tradeinfo']//div[@class='table-wrap table-onerow']

            PE = driver.find_element(By.XPATH, "//div[@id='info-tradeinfo']//div[@class='table-wrap table-onerow']/table/tbody")

            PE = PE.text.split(' ')[-3]


            sector, industry = sector.text.split("Basic Industry")[1].split(' ')[1], sector.text.split("Basic Industry")[1].split(' ')[2]
            # print(sector, indsutry)

            marketcap = element.text.split('Total Market Cap')[1].split(' ')[3].split('\n')[0]

            tradedValue = element.text.split('Traded Value')[1].split(' ')[3].split('\n')[0]

            print(sector, industry, tradedValue, PE)

            print(marketcap)

            break



            # *********** below code help to add records in database ********************

            # sql = """INSERT INTO stockalldata(stock_name, marketcap, sector, industry) VALUES(%s, %s, %s, %s ) """



            # conn = psycopg2.connect( database="stock", user='rohit', password='1234', host='localhost', port= '5432')
            # cur = conn.cursor()

            # cur.execute(sql, (stock_name, marketcap, sector, industry))

            # conn.commit()

            # ****************************************************************************************************
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            break

def fetchStockPrice(stock_name):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        val = "https://www.nseindia.com/get-quotes/equity?symbol={0}".format(stock_name)
        driver.get(val)
        time.sleep(3)
        sector = driver.find_element(By.XPATH, "/html/body/div[10]/div/div/section/div/div/div/div[1]/div/div[2]/div/section/div/div/div/aside[2]")
        current_sector_price = driver.find_element(By.XPATH, "//*[@id='quoteLtp']")


        print(sector.text.split('\n')[1].split(' ')[0],'???')
        last_price = float(sector.text.split('\n')[1].split(' ')[0])
        current_price  = float(current_sector_price.text)
        # current_price  = float(sector.text.split('\n')[1].split(' ')[4])



        # last_price, current_price = current_price, last_price


        print(last_price, current_price)
        print((current_price-last_price)/current_price*100)



fetchStockPrice("HCC")
# insert_listedcompany()
        

            





