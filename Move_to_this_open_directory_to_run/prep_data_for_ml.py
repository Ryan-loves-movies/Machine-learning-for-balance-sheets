from save_state.pickle_save import save_data_into_json, load_data_from_json
import time
import pickle
import pandas as pd
import numpy as np
from Classes.thread_requests import Connection, get_data
from all_stocks.all_stock_symb import all_stocks
import threading

def next_month(date):
    """
    date = 2018-12-31
    return 2019-1-31
    """
    split_date = date.split(sep='-')
    year = int(split_date[0])
    month = int(split_date[1])
    try:
        day = split_date[2]
    except:
        day = 31
    if month<12:
        return f'{year}-{month+1}-{day}'
    else:
        return f'{year+1}-{1}-{day}'

def extract_symb(string):
    new = ""
    for i in string:
        new += i
        if i.isdigit():
            new = new[:-1]
            return new

def add_balance_sheet_to_prices(file_name):
    balance_sheets = load_data_from_json("./balance_sheets/filtered_balance_sheets.json")
    stocks = [i for i in balance_sheets]
    ml_2018 = {}
    # ml_2018 = {'AAPL': {'date':... , 'Cash and cash equivalents':... , ...}, ...}
    for k in range(15):
        for i in balance_sheets:
            if len(balance_sheets[i]['financials'])>=k+1:
                financials2018 = balance_sheets[i]['financials'][k]
                ml_2018[(i+"{}yrs_ago").format(k)] = {element: financials2018[element] for element in financials2018}
    # filtered historical prices are only those with enough years to extract (>8years)
    # {'AAPL':{historical: [{date:... , close:...}, ...], ...}
    prices_to_extract = load_data_from_json("all_historical_prices_not_empty.json")

    to_pop = []
    for i in ml_2018:
        symb = extract_symb(i)
        # Only those whose prices can be found are included
        if symb in prices_to_extract:
            if prices_to_extract[symb] != {}:
                row = ml_2018[i]
                date_of_price = next_month(row['date'])
                look_up = prices_to_extract[symb]['historical']
                for k in look_up:
                    if k['date'] == date_of_price:
                        price = k['close']
                        ml_2018[i]['Price'] = price
                    elif k['date'].split(sep='-')[:-1] == date_of_price.split(sep='-')[:-1]:
                        price = k['close']
                        ml_2018[i]['Price'] = price
                    elif k['date'].split(sep='-')[0] == date_of_price.split(sep='-')[0]:
                        price = k['close']
                        ml_2018[i]['Price'] = price
        else:
            to_pop.append(i)
    for i in to_pop:
        ml_2018.pop(i)
    save_data_into_json(ml_2018, file_name)


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

def prep_data_into_dataframe(ml_2018, drop_na = False):
    """
    Will add new key, 'Price', to dict and remove previous "exact next month price"...
    Then, remove 'date' key in dictionary's dictionary
    Finally, convert all data to float instead of strings except for the date
    """
    ml_2018_copy = ml_2018.copy()
    for i in ml_2018:
        each = ml_2018[i]
        if 'Exact Next month price' in each:
            price = each['Exact Next month price']
            ml_2018_copy[i].pop('Exact Next month price')
            ml_2018_copy[i]['Price'] = price
        if 'Next month price' in each:
            price = each['Next month price']
            ml_2018_copy[i].pop('Next month price')
            ml_2018_copy[i]['Price'] = price
        if 'Same year price' in each:
            price = each['Same year price']
            ml_2018_copy[i].pop('Same year price')
            ml_2018_copy[i]['Price'] = price
        if not 'Price' in ml_2018_copy[i]:
            ml_2018_copy.pop(i)
    print(len([ml_2018_copy[i]['Price'] for i in ml_2018_copy]))
    for i in ml_2018_copy:
        ml_2018_copy[i].pop('date')
    for i in ml_2018_copy:
        for k in ml_2018_copy[i]:
            if ml_2018_copy[i][k]!="":
                ml_2018_copy[i][k] = np.float64(ml_2018_copy[i][k])
            else:
                ml_2018_copy[i][k] = None
    print(ml_2018_copy)
    df = pd.DataFrame.from_dict({k:pd.Series(v) for k,v in ml_2018_copy.items()}, orient = 'index')
    print(df)
    if drop_na == True:
        df = df.dropna()
    cols = [i for i in df.columns]
    cols.pop(-1)
    cols.pop(0)
    X = df[cols]
    Y = df['Price']
    return X,Y