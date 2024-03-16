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


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

val = "https://www.screener.in/company/RELIANCE/consolidated/"

driver.get(val)

time.sleep(2)

conn = psycopg2.connect(
   database="stock", user='rohit', password='1234', host='localhost', port= '5432'
)


def scrapAllFinicalData():

    table_element = driver.find_element(By.XPATH, "//section[@id='quarters']//div[@class='responsive-holder fill-card-width']")

    table_rows = table_element.find_elements(By.TAG_NAME, 'tr')

    # print(table_rows)

    # shareholding
    # quarters
    # profit-loss



    data_header = []

    for row in table_rows:
        row_data = []
        # Get the cells in each row
        cells = row.find_elements(By.TAG_NAME, 'th')
        # cells2 = row.find_elements(By.TAG_NAME, 'td')

        # print(cells.text)
        for cell in cells:
            # print(cell.text)
            row_data.append(cell.text)
        data_header.append(row_data)


    df_header = pd.DataFrame(data_header)


    # Print the DataFrame
    header = df_header[0:1]

    header = header.values.tolist()[0]





    data = []
    for row in table_rows:
        row_data = []
        # Get the cells in each row
        cells = row.find_elements(By.TAG_NAME, 'td')
        # cells2 = row.find_elements(By.TAG_NAME, 'td')

        # print(cells.text)
        for cell in cells:
            # print(cell.text)
            row_data.append(cell.text)
        data.append(row_data)

    # Convert data to a pandas DataFrame


    df = pd.DataFrame(data, columns=header)

    # Print the DataFrame
    # print(df,'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

    # print(type(a))
    df  = df[1:20:1]

    # print(df.values.tolist())

    # df = df.to_dict()

    # df.pop('', None)
    

    # print(df)


    
    # for key, values in df.items():
    #     print(key, '>>>')

    #     for k, v in values.items():
    #         print(v)

    addScrapData(header, df.values.tolist())


def addScrapData(header, df):

    # print(df)

    cur = conn.cursor()

    sql_query = """
    SELECT column_name FROM information_schema.columns WHERE table_name = 'quaterly';
    """

    # Execute the SQL query
    cur.execute(sql_query)

    # Fetch all rows from the result set
    rows = cur.fetchall()

    # Extract column names from the result set
    column_names = [row[0] for row in rows]


    # print(column_names)

    for head_column in header[1:]:
        if head_column not in column_names:
            print(head_column)
            sql_query = f'ALTER TABLE quaterly ADD COLUMN "{head_column}" VARCHAR(255);'

            # print(sql_query)
            cur.execute(sql_query)
            conn.commit()

        if head_column in column_names:
            
            for data in df:
                print(data)
            #     if head_column==key:
            #         new_list_data = []

                    
            #         for k, v in values.items():
            #             new_list_data.append(v)


            #         sql_query_inside = f'INSERT INTO quaterly ("{head_column}") VALUES (%s);'
            #         print(new_list_data,'>>>>>>>>>>>>>')

            #         # print(sql_query_inside)

            #         # Execute the SQL query with the list data values
            #         for value in new_list_data:
            #             cur.execute(sql_query_inside, ([value],))

            #         # Commit the transaction
            #         conn.commit()
                
                    
            
            




    # # Define your SQL query to add a new column
    # sql_query = "ALTER TABLE quaterly ADD COLUMN new_column_name data_type;"

    # # Execute the SQL query
    # cur.execute(sql_query)

    # # Commit the transaction
    # conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()



scrapAllFinicalData()




