from urllib.request import urlopen
import json

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
def get_request(symbol, url_to_format, new_dict):
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
    data = get_jsonparsed_data(url_to_format.format(symbol))
    print(f'{symbol} being processed')
    new_dict[f'{symbol}'] = data
def get_one_request(url):
    data = get_jsonparsed_data(url)
    print(f'{url} being processed')
    return data
