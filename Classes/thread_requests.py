from .fmp_requests import get_request, get_one_request
import threading
import json
from urllib.request import urlopen

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

def get_data(url_to_format, symbol, dict):
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
    stock = get_jsonparsed_data(url_to_format.format(symbol))
    print(f'{symbol} being processed')
    dict[f'{symbol}'] = stock

class Connection():
    def __init__(self):
        self.dictionary = {}
    def make_one_request(self, url):
        self.dictionary = get_one_request(url)
        print(f'Request to {url} in json format has been made!')
    def make_requests(self, url_to_format, stock_symbols):
        """
        Receive the content of `url`, parse it as JSON (Opened as dictionary),
        then saved in self.dictionary in the form {'AAPL': {...(Content)}, ... }

        Parameters
        ----------
        url_to_format : string to format url with
        stock_symbols : List of stock symbols

        Returns
        -------
        self.dictionary updated (with missing dictionaries removed)
        """
        threads = []
        for i in stock_symbols:
            t = threading.Thread(target = get_request, args = [i, url_to_format, self.dictionary])
            t.daemon = True
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join(timeout=20)
        print((str(len(stock_symbols) - len(self.dictionary)) + "\n\n\n\n\n\n\n")*10)
        # if len(stock_symbols) != len(self.dictionary):
        #
        #     to_update = [i for i in stock_symbols if i not in self.dictionary]
        #     self.make_requests(url_to_format, to_update)
        return self.dictionary
    # def fill_in_requests(self, url_to_format, stock_symbols):
