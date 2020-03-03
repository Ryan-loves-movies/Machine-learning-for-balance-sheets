from save_state.pickle_save import save_data_into_json, load_data_from_json
import time
import pickle
import pandas as pd
from Classes.thread_requests import Connection, get_data
from all_stocks.all_stock_symb import all_stocks
import threading


# Balance sheets and prices stocks intersection
# balance_sheets = load_data_from_json('balance_sheets/filtered_balance_sheets.json')
# prices = load_data_from_json('prices/all_current_prices.json')
# common = [i for i in balance_sheets if i in prices]
# balance_sheets = { i : balance_sheets[i]['financials'] for i in balance_sheets if i in common}

# Prices in dictionary
# prices = Connection()
# prices.make_one_request('https://financialmodelingprep.com/api/v3/stock/real-time-price')
# prices.dictionary = {i['symbol']:i['price'] for i in prices.dictionary['stockList']}
# print(prices.dictionary)

# Historical Prices
# historical_prices = Connection()
# historical_prices.make_requests("https://financialmodelingprep.com/api/v3/historical-price-full/{}?serietype=line", all_stocks)
# save_data_into_json(historical_prices.dictionary, "historical_prices_1.json")
# first_length = len(historical_prices.dictionary)

# with open("all_stocks/test.txt", "rb") as fp:
#     to_data = pickle.load(fp) # Unpickling
# start = time.time()
start = time.time()
historical_prices = load_data_from_json("historical_prices_full.json")
print(time.time()-start)
# filtered_historical_prices = {i:historical_prices[i] for i in to_data}
# save_data_into_json(filtered_historical_prices, "filtered_historical_prices.json")
# print(time.time() - start)
# print(len(historical_prices))
#   Filtered historical prices include only those with enough history and have non-empty balance sheets
historical_prices_copy = historical_prices.copy()
for i in historical_prices:
    if historical_prices[i] == {}:
        historical_prices_copy.pop(i)
print(time.time()-start)
save_data_into_json(historical_prices_copy,"all_historical_prices_not_empty.json")
print(time.time()-start)