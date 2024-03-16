import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt

# Calculate SMA

class StockTechincalData():

    def calculate_macd(data):
        # Calculate the 12-day and 26-day Exponential Moving Averages (EMAs)
        ema12 = data['Close'].ewm(span=12, min_periods=0, adjust=False).mean()
        ema26 = data['Close'].ewm(span=26, min_periods=0, adjust=False).mean()

        # Calculate the MACD line
        macd_line = ema12 - ema26

        # Calculate the Signal Line (9-day EMA of the MACD line)
        signal_line = macd_line.ewm(span=9, min_periods=0, adjust=False).mean()

        last_macd, last_signal = macd_line.iloc[-1], signal_line.iloc[-1]

        if last_macd > last_signal:
            return 'Bullish'
        elif last_macd < last_signal:
            return 'Bearish'
        else:
            return 'Neutral'

    def calculate_stoch(data, k_period=9, d_period=6):
        # Calculate the lowest low and highest high over the k_period
        low_min = data['Low'].rolling(window=k_period).min()
        high_max = data['High'].rolling(window=k_period).max()

        # Calculate %K
        k = ((data['Close'] - low_min) / (high_max - low_min)) * 100

        # Calculate %D
        d = k.rolling(window=d_period).mean()


        oversold_threshold=20
        overbought_threshold=80
        
        last_k, last_d = k.iloc[-1], d.iloc[-1]

        # print(last_k, last_d)

        if last_k < oversold_threshold:
            return 'Oversold'
        elif last_k > overbought_threshold:
            return 'Overbought'
        else:
            return 'Neutral'

    def calculate_rsi(data, window=14):
        delta = data['Close'].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        # print(rsi)
        return round(rsi[-1], 2)

    def calculate_sma(data, window1):
        for index,  value in enumerate(window1):
            window1[index] = round(data['Close'].rolling(window=value).mean()[-1],2)

        return window1


    # Calculate EMA
    def calculate_ema(data, window):
        for index,  value in enumerate(window):
            window[index] = round(data['Close'].ewm(span=value, adjust=False).mean()[-1],2)

        return window

    def main(name):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        ticker_symbol = name+'.NS'  # Example: Apple Inc.

        # Define the time period for which you want to fetch data
        start_date = '2000-01-01'
        end_date = datetime.today().strftime('%Y-%m-%d')

        # Fetch historical data from Yahoo Finance
        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

        # print(stock_data)

        window_list  = [5,10,20,50,100,200]

        sma_data = StockTechincalData.calculate_sma(stock_data, window_list)
        # print(sma_data)

        ema_data = StockTechincalData.calculate_ema(stock_data, [5,10,20,50,100,200]) 
        
        # print(ema_data)

        rsi = StockTechincalData.calculate_rsi(stock_data)

        signal_stoch = StockTechincalData.calculate_stoch(stock_data)

        signal_macd  =StockTechincalData.calculate_macd(stock_data)

        # print(signal_macd)

        return sma_data, ema_data, rsi, signal_stoch, signal_macd


# StockTechincalData.main(name='SBIN')
# print(sma_data, ema_data)




# # Plotting
# plt.figure(figsize=(14, 7))
# plt.plot(stock_data['Close'], label='Close Price', color='blue')
# plt.plot(stock_data['SMA'], label='SMA (20)', color='orange')
# plt.plot(stock_data['EMA'], label='EMA (20)', color='red')
# plt.legend(loc='upper left')
# plt.show()

