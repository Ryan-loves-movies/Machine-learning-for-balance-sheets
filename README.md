# Machine-learning-for-balance-sheets
So..., let's begin!
I approached this project in 5 phases -- 

## 1.) Obtaining info from website

For this, I used the api of the website, 'financialmodelingprep.com', to obtain all the stock symbols. 
This was short and sweet. Just these few lines were sufficient. (Under the all_stocks file)
```python
import requests

available_stocks = requests.get("https://financialmodelingprep.com/api/v3/company/stock/list")
all_stocks = [i['symbol'] for i in available_stocks.json()['symbolsList']]
```

Then, I used this information to obtain the balance sheets and historical prices of all the stocks available on the website. The code I used is in the Classes file: the fmp_requests.py file is only used as support for the thread_requests.py file. 
```python
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
```
This is the class I created to make the requests to the website to obtain the various types of data. To anyone out there who is just starting out trying to do something similar, this was the fastest method that worked for me.

## 2.) Storing info into a dictionary format
This part wasn't too difficult
```python
def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)
def get_balance_sheet(symbol, dict):
    stock = get_jsonparsed_data(balance_sheet_link.format(symbol))
    print(f'{symbol} being processed')
    dict[f'{symbol}'] = stock
```
Used this code for the threading mentioned before so data is already in correct format once saved.

## 3.) Filtering the info I obtained
Removing those stocks with empty data.
```python
balance_sheets = load_data_from_json('balance_sheets/full_balance_sheet_list.json')
filtered_dict = { i : balance_sheets[i] for i in balance_sheets if balance_sheets[i]!={}}
save_data_into_json(filtered_dict, 'filtered_balance_sheets.json')
```

## 4.) Preprocessing the data
Putting the data together, then converting all the data into a dataframe.
This part is in prep_data_for_ml.py in the folder that reads 'Move_to_this_open_directory_to_run'.
```python
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
```
I realised this could be much shorter but... meh, I think I wanna move on to something new and read up more about finance before looking back on all this work. Bless anyone who actually read and understood that fully. I'm so sorry!

## 5.) Finally Actual Machine Learning!! WOO!!
Finally, actually doing some machine learning using RandomForestRegressor and XGBoost to predict the prices from the data.
This part is in ml_try.py in the folder that reads 'Move_to_this_open_directory_to_run'.

```python
def optimise_random_forest(x_train,x_test,y_train,y_test):
    mae = {}
    for i in [100]:
        random_forest = RandomForestRegressor(random_state = 0, n_estimators = i, min_samples_leaf = 2)
        random_forest.fit(x_train,y_train)
        predictions = random_forest.predict(x_test)
        mae[i] = mean_absolute_error(predictions,y_test)
    return mae
dict_of_mae = optimise_random_forest(x_train,x_test,y_train,y_test)

def optimise_xgb(x_train,x_test,y_train,y_test):
    mae = {}
    for i in [100]:
        xgb = XGBRegressor(n_estimators=i, early_stopping_rounds=5, eval_set=[(x_test, y_test)])
        xgb.fit(x_train,y_train)
        predictions = xgb.predict(x_test)
        mae[i] = mean_absolute_error(predictions,y_test)
    return mae

dict_of_mae = optimise_xgb(x_train,x_test,y_train,y_test)
print(dict_of_mae)
```
And finally, after roughly a month, we get some results that seem disappointing -- mae of 393.8 between the actual and predicted prices! Hahaha, welp! Hey, at least I finally got to trying out my first python project! 

### Any tips or suggestions on how to improve my code or how to move forward are greatly appreciated!!
