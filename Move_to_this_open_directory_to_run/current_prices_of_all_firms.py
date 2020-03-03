# 1.) Setting up of environment by importing all relevant modules

import time
from urllib.request import urlopen
import json
import threading
import concurrent.futures

from save_state.pickle_save import save_data_into_json, load_data_from_json

from debt_comparison.convert_finance_num import convert_num
# Convert 1.00e+11 to 1000000000...

from all_stocks.all_stock_symb import all_stocks
# Import an array of all the stocks available via the links --> ['SPY', 'AAPL', ...]

# 2.) Define the prices link as a variable
price_url = 'https://financialmodelingprep.com/api/v3/stock/real-time-price'

# 3.) Defining of all functions to be used in this main folder
start = time.time()

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """

    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

if __name__ == "__main__":
    prices = get_jsonparsed_data(price_url)
    price_list = prices['stockList']
    dict = {}
    for i in price_list:
        symbol = i['symbol']
        price = i['price']
        dict[f'{symbol}'] = float(price)
    save_data_into_json(dict, 'list_of_prices_2302.json')
    print(time.time() - start)