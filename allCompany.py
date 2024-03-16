from flask import Flask, render_template
import psycopg2
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
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import Flask, render_template, request, jsonify, redirect
from StockTechincalData import StockTechincalData


# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager



app = Flask(__name__)
def fetchStockPrice(stock_name):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        
        val = "https://www.nseindia.com/get-quotes/equity?symbol={0}".format(stock_name)
        driver.get(val)
        time.sleep(3)
        sector = driver.find_element(By.XPATH, "/html/body/div[11]/div/div/section/div/div/div/div[1]/div/div[2]/div/section/div/div/div/aside[2]")
        
        current_sector_price = driver.find_element(By.XPATH, "//*[@id='quoteLtp']")
        

        print(sector.text)

        print(sector.text.split('\n')[1].split(' ')[0],'???')
        last_price = float((sector.text.split('\n')[1].split(' ')[0]).replace(",", "").replace(".", ""))
        current_price  = float((current_sector_price.text).replace(",", "").replace(".", ""))
        # current_price  = float(sector.text.split('\n')[1].split(' ')[4])



        # last_price, current_price = current_price, last_price


        print(last_price, current_price)
        print(type((current_price-last_price)/current_price*100))

        return current_price, last_price, round(float((current_price-last_price)/current_price*100),3)

@app.route('/suggest', methods=['POST','GET'])
def suggest():

    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            return redirect(f'/company/{query}')
        else:
            return "Invalid search query"
    else:

        query = request.args.get('query', '').lower()

        try:
            # Connect to PostgreSQL database
            conn = psycopg2.connect( database="stock", user='rohit', password='1234', host='localhost', port= '5432')
            cursor = conn.cursor()
            # postgreSQL_select_Query = "select * from stockalldata"

            cursor.execute("SELECT stock_name FROM stockalldata WHERE LOWER(stock_name) LIKE %s", ('%' + query + '%',))
            # cursor.execute(postgreSQL_select_Query)
            suggestions = [row[0] for row in cursor.fetchall()]

            # Close cursor and connection
            cursor.close()
            conn.close()
            # Prevent caching on client side

            print(suggestions,"user_profile")

            # user_profile(suggestions)

            return jsonify({'suggestions': suggestions})

        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)
            return jsonify({'error': 'Database error'})



def create_bar_chart(products, products_q, key_data, data, title):
    if key_data=='profit-loss':
        products = products_q

    print(products, data, key_data,'????????????????????????')
    plt.figure(figsize=(6, 6))
    # plt.bar(products, data, color='skyblue')
    plt.bar(products, data, color=['skyblue' if int(s) >= 0 else 'red' for s in data])
    plt.title(title)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # print('YES')
    return graphic

def drawBarChart(data, categories, name, market_cap, book_value, symbol, top_list, list1, list2, rsi, signal_stoch, signal_macd):

    # print(data)

    print(list1, list2)

    values = []

    sales_quater = []
    expenses_qauter = []
    margin_quater = []
    netprofit_quater = []


    data = json.loads(data)

    closed_price, last_price, per = fetchStockPrice(name)

    # print(closed_price, last_price, per, "nameeeeeeeeeeee")
    # print(data)

    # data  = {"quarters": {"": {"1": "Sales +", "2": "Expenses +", "3": "Operating Profit", "4": "OPM %", "5": "Other Income +", "6": "Interest", "7": "Depreciation", "8": "Profit before tax", "9": "Tax %", "10": "Net Profit +", "11": "EPS in Rs", "12": "Raw PDF"}, "Dec 2020": {"1": "772", "2": "1,325", "3": "-553", "4": "-72%", "5": "76", "6": "9", "7": "38", "8": "-525", "9": "-2%", "10": "-536", "11": "-88.46", "12": ""}, "Mar 2021": {"1": "815", "2": "1,310", "3": "-495", "4": "-61%", "5": "96", "6": "7", "7": "51", "8": "-456", "9": "3%", "10": "-444", "11": "-73.04", "12": ""}, "Jun 2021": {"1": "891", "2": "1,274", "3": "-383", "4": "-43%", "5": "55", "6": "10", "7": "41", "8": "-379", "9": "-1%", "10": "-382", "11": "-6.31", "12": ""}, "Sep 2021": {"1": "1,086", "2": "1,545", "3": "-459", "4": "-42%", "5": "48", "6": "10", "7": "50", "8": "-472", "9": "-0%", "10": "-474", "11": "-7.76", "12": ""}, "Dec 2021": {"1": "1,456", "2": "2,244", "3": "-788", "4": "-54%", "5": "88", "6": "12", "7": "61", "8": "-773", "9": "-1%", "10": "-778", "11": "-12.01", "12": ""}, "Mar 2022": {"1": "1,541", "2": "2,308", "3": "-767", "4": "-50%", "5": "108", "6": "7", "7": "95", "8": "-762", "9": "-0%", "10": "-762", "11": "-11.74", "12": ""}, "Jun 2022": {"1": "1,680", "2": "2,320", "3": "-640", "4": "-38%", "5": "102", "6": "6", "7": "97", "8": "-641", "9": "-1%", "10": "-645", "11": "-9.93", "12": ""}, "Sep 2022": {"1": "1,914", "2": "2,461", "3": "-547", "4": "-29%", "5": "100", "6": "5", "7": "104", "8": "-557", "9": "-3%", "10": "-572", "11": "-8.80", "12": ""}, "Dec 2022": {"1": "2,062", "2": "2,393", "3": "-331", "4": "-16%", "5": "83", "6": "5", "7": "124", "8": "-377", "9": "-4%", "10": "-392", "11": "-6.04", "12": ""}, "Mar 2023": {"1": "2,334", "2": "2,466", "3": "-131", "4": "-6%", "5": "130", "6": "7", "7": "160", "8": "-168", "9": "0%", "10": "-168", "11": "-2.66", "12": ""}, "Jun 2023": {"1": "2,342", "2": "2,652", "3": "-311", "4": "-13%", "5": "123", "6": "7", "7": "159", "8": "-354", "9": "-1%", "10": "-358", "11": "-5.63", "12": ""}, "Sep 2023": {"1": "2,519", "2": "2,750", "3": "-231", "4": "-9%", "5": "139", "6": "7", "7": "180", "8": "-279", "9": "-5%", "10": "-292", "11": "-4.58", "12": ""}, "Dec 2023": {"1": "2,850", "2": "3,014", "3": "-163", "4": "-6%", "5": "149", "6": "5", "7": "201", "8": "-221", "9": "-0%", "10": "-222", "11": "-3.46", "12": ""}}, "profit-loss": {"": {"1": "Sales +", "2": "Expenses +", "3": "Operating Profit", "4": "OPM %", "5": "Other Income +", "6": "Interest", "7": "Depreciation", "8": "Profit before tax", "9": "Tax %", "10": "Net Profit +", "11": "EPS in Rs", "12": "Dividend Payout %"}, "Mar 2015": {"1": "323", "2": "683", "3": "-360", "4": "-111%", "5": "16", "6": "2", "7": "21", "8": "-367", "9": "-1%", "10": "-372", "11": "-123.02", "12": "0%"}, "Mar 2016": {"1": "855", "2": "2,523", "3": "-1,668", "4": "-195%", "5": "164", "6": "1", "7": "28", "8": "-1,534", "9": "-0%", "10": "-1,535", "11": "-331.99", "12": "0%"}, "Mar 2019": {"1": "3,224", "2": "7,592", "3": "-4,368", "4": "-135%", "5": "280", "6": "38", "7": "112", "8": "-4,237", "9": "0%", "10": "-4,231", "11": "-726.78", "12": "0%"}, "Mar 2020": {"1": "3,279", "2": "5,964", "3": "-2,685", "4": "-82%", "5": "-45", "6": "54", "7": "174", "8": "-2,958", "9": "1%", "10": "-2,942", "11": "-470.27", "12": "0%"}, "Mar 2021": {"1": "2,801", "2": "4,640", "3": "-1,838", "4": "-66%", "5": "356", "6": "38", "7": "178", "8": "-1,698", "9": "-0%", "10": "-1,701", "11": "-280.42", "12": "0%"}, "Mar 2022": {"1": "4,974", "2": "7,358", "3": "-2,384", "4": "-48%", "5": "288", "6": "42", "7": "247", "8": "-2,385", "9": "-0%", "10": "-2,396", "11": "-36.90", "12": "0%"}, "Mar 2023": {"1": "7,990", "2": "9,634", "3": "-1,644", "4": "-21%", "5": "410", "6": "24", "7": "485", "8": "-1,743", "9": "-2%", "10": "-1,776", "11": "-28.02", "12": "0%"}, "TTM": {"1": "10,045", "2": "10,882", "3": "-836", "4": "-8%", "5": "540", "6": "26", "7": "700", "8": "-1,022", "9": "", "10": "-1,039", "11": "-16.33", "12": ""}}, "shareholding": {"": {"1": "FIIs +", "2": "DIIs +", "3": "Public +", "4": "No. of Shareholders"}, "Dec 2021": {"1": "9.36%", "2": "1.06%", "3": "89.58%", "4": "10,57,586"}, "Mar 2022": {"1": "4.42%", "2": "1.07%", "3": "94.51%", "4": "12,59,775"}, "Jun 2022": {"1": "5.45%", "2": "1.15%", "3": "93.40%", "4": "11,95,332"}, "Sep 2022": {"1": "77.26%", "2": "1.33%", "3": "21.42%", "4": "11,24,470"}, "Dec 2022": {"1": "72.80%", "2": "1.87%", "3": "25.32%", "4": "12,00,100"}, "Mar 2023": {"1": "71.83%", "2": "3.19%", "3": "24.98%", "4": "11,20,566"}, "Jun 2023": {"1": "72.11%", "2": "3.54%", "3": "24.35%", "4": "10,34,995"}, "Sep 2023": {"1": "60.92%", "2": "4.05%", "3": "35.02%", "4": "10,12,892"}, "Dec 2023": {"1": "63.72%", "2": "6.07%", "3": "30.22%", "4": "11,28,929"}}}

    chart4 = 1
    chart5 = 1
    chart6 = 1
    index = 1
    for key, value in data.items():
        print(key,"keyyyyyyyyyyyyyyyyyy")
        if key!='shareholding':
            sales_quater = []
            expenses_qauter = []
            margin_quater = []
            netprofit_quater = []
            print('firstttttttttttttttttttttt')
            for i, (k, v) in enumerate(value.items()):
                if i!=0:
                    if len(v)>6:
                            
                        # print(k,"okeyyyyyyyyyyyyyyyy")
                        # print(v,"vvvvvvvvvvvvvvvvvvvvvv")
                        # print(v[str(index)],"valueeeeeeeeeeeeee")

                        sales_quater.append(v[str(index)])
                        expenses_qauter.append(v[str(index+1)])
                        margin_quater.append(v[str(index+3)])
                        # print(v,"okkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
                        
                        netprofit_quater.append(v[str(index+9)])
                        # print(netprofit_quater,'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

                    # print(sales_quater,"okkkkkkkkkkkkkk")

            # print(sales_quater)
            # print(expenses_qauter)
            # print(margin_quater)
            # print(netprofit_quater)

            sales_quater = [int(x.replace(',', '')) for x in sales_quater]
            expenses_qauter = [int(x.replace(',', '')) for x in expenses_qauter]
            # margin_quater = [int(x).replace(',', '') for x in margin_quater]
            netprofit_quater = [int(x.replace(',', '')) for x in netprofit_quater]

            # categories = ['1','2','3','4','5','6','7','8','9','10','11','12','13']

            header_p = []
            header_q = []
            header_s = []
            iter = 0
            last_profit_result = 0

            for k_inside, v_inside in data.items():
                iter = iter + 1
                for k_in, v_in in v_inside.items():
                    if iter==1 and k_in!='':
                        header_p.append(k_in)
                        
                    elif iter==2 and k_in!='':
                        header_q.append(k_in)
                        last_profit_result = v_in
                    elif iter==3 and k_in!='':
                        header_s.append(k_in)

            chart1 = create_bar_chart(header_q,header_p, key,sales_quater, "Sales")
            chart2 = create_bar_chart(header_q,header_p, key, expenses_qauter, "Expenses")
            chart3  = create_bar_chart(header_q,header_p, key,netprofit_quater, "Net Profit")

            if chart4==1:
                chart4 = chart1
                chart5=chart2
                chart6=chart3
        


            # print()
            # print(last_profit_result['10'],"header_p
            PE = last_profit_result['10'].replace(",", "")
            PE = int(PE)
            PE = round((market_cap/PE), 1)
            if PE<0:
                PE = 0

            
            PB  = round((closed_price/book_value),2)
            if PB<0:
                PB = 0

            print(rsi,"book value")
            

                
            

    return render_template('barchart.html', chart1=chart1, chart2=chart2, chart3=chart3, chart4=chart4, chart5=chart5, chart6=chart6, closed_price=closed_price, last_price=last_price, per=per, PE=PE, PB=PB, symbol=symbol, top_list=top_list, list1=list1, list2=list2, rsi=rsi, signal_stoch=signal_stoch, signal_macd=signal_macd)


        # Create bar chart
        # plt.bar(categories, expenses_qauter, color=['skyblue' if int(s) >= 0 else 'lightcoral' for s in expenses_qauter
        #                                              ])
        
        # fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        # Create the first bar chart
        # axs[0].bar(categories, sales_quater, color='skyblue')
        # axs[0].set_title('Sales Data Quaterly')

        # # Create the second bar chart
        # axs[1].bar(categories, expenses_qauter, color='salmon')
        # axs[1].set_title('Exepenses')

        # # Create the third bar chart
        # axs[2].bar(categories, netprofit_quater, color='lightgreen')
        # axs[2].set_title('Net Profit')


        # # Add labels and title
        # plt.xlabel('Categories')
        # plt.ylabel('Sales')
        # plt.title('Bar Chart Example')

        # # Show the plot
        # plt.show()
                    


# Dummy data for demonstration purposes

def getCompany():
    conn = psycopg2.connect( database="stock", user='rohit', password='1234', host='localhost', port= '5432')
    cursor = conn.cursor()
    postgreSQL_select_Query = "select * from stockalldata"
    cursor.execute(postgreSQL_select_Query)
    data = cursor.fetchall()

    return data

# print(data)


# Define a route to render the HTML page
@app.route('/', methods=['GET'])
def index():
    # Pass the data to the HTML template
    conn = psycopg2.connect( database="stock", user='rohit', password='1234', host='localhost', port= '5432')
    cursor = conn.cursor()
    postgreSQL_select_Query = "select * from stockalldata"
    cursor.execute(postgreSQL_select_Query)
    data = cursor.fetchall()
    # print(data)
    return render_template('index.html', data=data)


@app.route('/company/<string:name>')
def user_profile(name):
    sma_data, ema_data, rsi, signal_stoch, signal_macd = StockTechincalData.main(name)
    top_list = ['', 5,10,20,50,100,200]
    sma_data.insert(0,'SMA')
    ema_data.insert(0,'EMA')
    

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    val = f'https://www.screener.in/company/{name}/consolidated/'

    print(val)

    driver.get(val)

    time.sleep(2)

    conn = psycopg2.connect(
    database="stock", user='rohit', password='1234', host='localhost', port= '5432'
    )

    #/html/body/main/div[3]/div[3]/div[2]/ul/li[1]/span[2]/span

    market_cap = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[3]/div[2]/ul/li[1]/span[2]/span")
    market_cap = market_cap.text

    market_cap = market_cap.replace(",", "").replace(".", "")
    market_cap = int(market_cap)

    book_value = driver.find_element(By.XPATH, "/html/body/main/div[3]/div[3]/div[2]/ul/li[5]/span[2]/span")
    book_value = book_value.text

    book_value = book_value.replace(",", "").replace(".", "")
    book_value = int(book_value)

    

    col_data  = ["quarters", "profit-loss", "shareholding"]

    main_dict = {}

    for id_col in col_data:

        print("//section[@id='{}']//div[@class='responsive-holder fill-card-width']".format(id_col))


        table_element = driver.find_element(By.XPATH, "//section[@id='{}']//div[@class='responsive-holder fill-card-width']".format(id_col))

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

        # print(header,'??????????????????')

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

        # main_list.append(df.to_dict())

        # df = json.dumps((df.to_dict()))

        main_dict[id_col] = df.to_dict()

        # main_dict = json.dumps(main_dict)

        # drawBarChart(main_dict, header)
        # print(json.dumps(main_dict))
    return drawBarChart(json.dumps(main_dict), header, name, market_cap, book_value, name, top_list, sma_data, ema_data, rsi, signal_stoch, signal_macd)

if __name__ == '__main__':
    app.run(debug=True)
