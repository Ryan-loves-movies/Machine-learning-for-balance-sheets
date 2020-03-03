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

# from balance_sheet_prep import balance_sheet_link
# Import balance_sheet_link that contains the constant part of the link to get the balance sheet accounts
# E.g. "financialmodellingprep.com/jsdsndnan/sdj/?" --> Link would be "financialmodellingprep.com/jsdsndnan/sdj/?AAPL"



# 2.) First try at asynchronous requesting of data: Bad -- Too inefficient and no timeout function
# Failed start at extracting balance sheets through compiled threading
# This is a lot slower and more inefficient for some reason
# if __name__ == '__main__':

    # all_balance_sheets = {}
    #
    # start = time.time()
    #
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     executor.map(get_balance_sheet, all_stocks[:1000])
    #
    # end = time.time()
    # print(end-start)
    # save_data_into_json(all_balance_sheets, filename = "all_balance_sheets.json")
    # print("all done")



# 3.) Defining of all functions to be used in this main folder

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

def get_balance_sheet(symbol, dict):
    """
    Receive the content of the url of the stock and appends it to the "all_balance_sheets" dictionary
    that contains the key of the symbol of the stock called and content of url

    Parameters
    ---------
    symbol : str (containing stock symbol)
    dict : dictionary to append to

    Function
    ---------
    Appends to end of "all_balance_sheets" dictionary

    """
    stock = get_jsonparsed_data(balance_sheet_link.format(symbol))
    print(f'{symbol} being processed')
    dict[f'{symbol}'] = stock





# 4.) Extracting all balance sheets in 2 batches through threading manually: Great -- A lot more efficient!!

# all_balance_sheets = {}
#
# start = time.time()
#
# threads = []

# for i in all_stocks[:7000]:
#     t = threading.Thread(target = get_balance_sheet, args = [i])
#     t.daemon = True
#     t.start()
#     threads.append(t)

# for thread in threads:
#     thread.join(timeout=20)

# for i in all_stocks[7000:]:
#     t = threading.Thread(target = get_balance_sheet, args = [i])
#     t.daemon = True
#     t.start()
#     threads.append(t)
#
# for thread in threads:
#     thread.join(timeout=20)
#
# end = time.time()
# print(end-start)
# save_data_into_json(all_balance_sheets, filename = "all_balance_sheets_2.json")
# print("all done")

# 5.) Compilation of the 2 sets of data into 1 compiled file -- Didn't want to do all in one so that time could be saved
# if one thread stopped the rest and slowed everything down. (Debugging purposes)

# all_balance_sheets_1 = load_data_from_json("all_balance_sheets.json")
# all_balance_sheets_2 = load_data_from_json("all_balance_sheets_2.json")
# for i in all_balance_sheets_1:
#     all_balance_sheets_2[i] = all_balance_sheets_1[i]
# save_data_into_json(all_balance_sheets_2, "all_balance_sheets_compiled.json")



# 6.) Storing the list of missed stocks -- i.e. Those that couldn't load before and slowed the threading

# all_balance_sheets_compiled = load_data_from_json("all_balance_sheets_compiled.json")
# missed_out = [i for i in all_stocks if i not in all_balance_sheets_compiled]
#
# missed_dict = {}
#
# threads = []
#
    # for i in missed_out:
    #     t = threading.Thread(target = get_balance_sheet, args = [i, missed_dict])
    #     t.daemon = True
    #     t.start()
    #     threads.append(t)
    #
    # for thread in threads:
    #     thread.join()
    #
    # save_data_into_json(missed_dict, "missed_out_bs.json")



# 7.) Final Compilation of all stocks' balance sheets

# compiled_before = load_data_from_json("all_balance_sheets_compiled.json")
# missed_out = load_data_from_json("missed_out_bs.json")
# for i in missed_out:
#     compiled_before[i] = missed_out[i]
# save_data_into_json(compiled_before, "full_balance_sheet_list.json")




prices
'AWX': {'symbol': 'AWX', 'historical': [{'date': '1998-06-23', 'close': 6.25}, {'date': '1998-06-24', 'close': 6.75}, {'date': '1998-06-25', 'close': 7.56}, {'date': '1998-06-26', 'close': 7.38}, {'date': '1998-06-29', 'close': 7.0}, {'date': '1998-06-30', 'close': 6.63}, {'date': '1998-07-01', 'close': 6.94}, {'date': '1998-07-02', 'close': 6.94}, {'date': '1998-07-06', 'close': 6.81}, {'date': '1998-07-07', 'close': 7.13}, {'date': '1998-07-08', 'close': 7.0}, {'date': '1998-07-09', 'close': 6.94}, {'date': '1998-07-10', 'close': 7.06}, {'date': '1998-07-13', 'close': 7.06}, {'date': '1998-07-14', 'close': 7.25}, {'date': '1998-07-15', 'close': 7.0}, {'date': '1998-07-16', 'close': 7.19}, {'date': '1998-07-17', 'close': 7.19}, {'date': '1998-07-20', 'close': 7.38}, {'date': '1998-07-21', 'close': 7.5}, {'date': '1998-07-22', 'close': 7.5}, {'date': '1998-07-23', 'close': 7.63}, {'date': '1998-07-24', 'close': 7.63}, {'date': '1998-07-27', 'close': 7.75}, {'date': '1998-07-28', 'close': 7.69}, {'date': '1998-07-29', 'close': 7.5}, {'date': '1998-07-30', 'close': 7.75}, {'date': '1998-07-31', 'close': 7.56}, {'date': '1998-08-03', 'close': 7.44}, {'date': '1998-08-04', 'close': 7.06}, {'date': '1998-08-05', 'close': 6.88}, {'date': '1998-08-06', 'close': 7.0}, {'date': '1998-08-07', 'close': 6.88}, {'date': '1998-08-10', 'close': 7.0}, {'date': '1998-08-11', 'close': 6.88}, {'date': '1998-08-12', 'close': 7.0}, {'date': '1998-08-13', 'close': 7.13}, {'date': '1998-08-14', 'close': 8.0}, {'date': '1998-08-17', 'close': 9.0}, {'date': '1998-08-18', 'close': 9.25}, {'date': '1998-08-19', 'close': 9.19}, {'date': '1998-08-20', 'close': 8.94}, {'date': '1998-08-21', 'close': 8.81}, {'date': '1998-08-24', 'close': 9.06}, {'date': '1998-08-25', 'close': 8.88}, {'date': '1998-08-26', 'close': 8.56}, {'date': '1998-08-27', 'close': 8.5}, {'date': '1998-08-28', 'close': 8.44}, {'date': '1998-08-31', 'close': 8.38}, {'date': '1998-09-01', 'close': 8.38}, {'date': '1998-09-02', 'close': 8.13}, {'date': '1998-09-03', 'close': 8.0}, {'date': '1998-09-04', 'close': 8.13}, {'date': '1998-09-08', 'close': 8.0}, {'date': '1998-09-09', 'close': 8.25}, {'date': '1998-09-10', 'close': 7.88}, {'date': '1998-09-11', 'close': 7.75}, {'date': '1998-09-14', 'close': 8.0}, {'date': '1998-09-15', 'close': 8.0}, {'date': '1998-09-16', 'close': 8.0}, {'date': '1998-09-17', 'close': 8.0}, {'date': '1998-09-18', 'close': 8.13}, {'date': '1998-09-21', 'close': 8.0}, {'date': '1998-09-22', 'close': 8.31}, {'date': '1998-09-23', 'close': 8.25}, {'date': '1998-09-24', 'close': 8.25}, {'date': '1998-09-25', 'close': 8.38}, {'date': '1998-09-28', 'close': 8.25}, {'date': '1998-09-29', 'close': 8.13}, {'date': '1998-09-30', 'close': 8.5}, {'date': '1998-10-01', 'close': 7.81}, {'date': '1998-10-02', 'close': 7.88}, {'date': '1998-10-05', 'close': 7.75}, {'date': '1998-10-06', 'close': 7.69}, {'date': '1998-10-07', 'close': 7.63}, {'date': '1998-10-08', 'close': 7.63}, {'date': '1998-10-09', 'close': 7.5}, {'date': '1998-10-12', 'close': 7.5}, {'date': '1998-10-13', 'close': 7.5}, {'date': '1998-10-14', 'close': 7.44}, {'date': '1998-10-15', 'close': 7.5}, {'date': '1998-10-16', 'close': 7.5}, {'date': '1998-10-19', 'close': 7.38}, {'date': '1998-10-20', 'close': 7.63}, {'date': '1998-10-21', 'close': 7.56}, {'date': '1998-10-22', 'close': 7.56}, {'date': '1998-10-23', 'close': 7.5}, {'date': '1998-10-26', 'close': 7.5}, {'date': '1998-10-27', 'close': 7.63}, {'date': '1998-10-28', 'close': 7.69}, {'date': '1998-10-29', 'close': 7.69}, {'date': '1998-10-30', 'close': 8.06}, {'date': '1998-11-02', 'close': 7.75}, {'date': '1998-11-03', 'close': 8.0}, {'date': '1998-11-04', 'close': 8.13}, {'date': '1998-11-05', 'close': 8.0}, {'date': '1998-11-06', 'close': 8.19}, {'date': '1998-11-09', 'close': 8.25}, {'date': '1998-11-10', 'close': 8.13}, {'date': '1998-11-11', 'close': 8.0}, {'date': '1998-11-12', 'close': 8.0}, {'date': '1998-11-13', 'close': 7.88}, {'date': '1998-11-16', 'close': 7.94}, {'date': '1998-11-17', 'close': 7.88}, {'date': '1998-11-18', 'close': 7.88}, {'date': '1998-11-19', 'close': 7.75}, {'date': '1998-11-20', 'close': 7.78}, {'date': '1998-11-23', 'close': 7.75}, {'date': '1998-11-24', 'close': 7.75}, {'date': '1998-11-25', 'close': 7.94}, {'date': '1998-11-27', 'close': 7.94}, {'date': '1998-11-30', 'close': 7.81}, {'date': '1998-12-01', 'close': 7.75}, {'date': '1998-12-02', 'close': 7.88}, {'date': '1998-12-03', 'close': 7.75}, {'date': '1998-12-04', 'close': 7.63}, {'date': '1998-12-07', 'close': 7.63}, {'date': '1998-12-08', 'close': 7.63}, {'date': '1998-12-