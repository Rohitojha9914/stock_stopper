import requests
from lxml import html
from bs4 import BeautifulSoup

url = 'https://www.livemint.com/market/stock-market-news/dividend-stocks-3-stocks-account-nearly-half-of-warren-buffets-dividend-income-apple-oxy-bofa-11688894392423.html'

r = requests.get(url)

soup = BeautifulSoup(r.text,"html.parser")

results = soup.findAll(True, {'class':['contentSec']})

# print(results)

print(">>>>>>")
records = []  
for result in results:  
    p1 = result.find('div', attrs={'class':'mainArea'}).text # result not results
    p2 = result.find('div', attrs={'class':'FirstEle'}).text
    records.append((p1, p2,))



print(records)
print(">>>")
