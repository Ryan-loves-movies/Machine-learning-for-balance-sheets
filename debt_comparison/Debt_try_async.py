import statistics
import time
from urllib.request import urlopen
import json
import concurrent.futures

from convert_finance_num import convert_num
# Convert 1.00e+11 to 1000000000...

from all_stock_symb import all_stocks, tasks
# Import an array of all the stocks available via the links --> ['SPY', 'AAPL', ...]

from balance_sheet_prep import balance_sheet_link
# Import balance_sheet_link that contains the constant part of the link to get the balance sheet accounts
# E.g. "financialmodellingprep.com/jsdsndnan/sdj/?" --> Link would be "financialmodellingprep.com/jsdsndnan/sdj/?AAPL"

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

def debt_filter(symbol):
    stock = get_jsonparsed_data(balance_sheet_link.format(symbol))
    if stock != {}:
        stock_financials = stock['financials'][0]
        debt = convert_num(stock_financials['Total debt'])
        debt_avg.append(debt)
        if debt == 0:
            debt_free.append(symbol)


debt_free = []
debt_avg = []
start = time.time()

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(debt_filter, all_stocks)

end = time.time()

print(debt_free)
print(debt_avg)

with open('debt_free_final.txt','w') as f:
    for i in debt_free:
        f.write(i + " ")

with open('debt_avg_final.txt','w') as f:
    for i in debt_avg:
        f.write(str(i) + " ")