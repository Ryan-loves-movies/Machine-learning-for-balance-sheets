import requests

available_stocks = requests.get("https://financialmodelingprep.com/api/v3/company/stock/list")
all_stocks = [i['symbol'] for i in available_stocks.json()['symbolsList']]

# all_stocks = All stocks available from the financial modelling prep website

