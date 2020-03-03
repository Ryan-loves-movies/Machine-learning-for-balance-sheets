from pickle_save import load_data_from_json
import pickle

# Dates: to see the number of stocks with sufficient historical data
itera = 2020
no = 0
dates = {}
balance_sheets = load_data_from_json("filtered_balance_sheets.json")

for symb in balance_sheets:
    balance_sheet = balance_sheets[symb]
    no_of_dates = []
    for year in balance_sheet['financials']:
        no_of_dates.append(year['date'])
    dates[symb] = no_of_dates

dates_no = {i:len(dates[i]) for i in dates}

to_data = []
for i in dates_no:
    if dates_no[i]>7:
        to_data.append(i)

with open("test.txt", "wb") as fp:   #Pickling
    pickle.dump(to_data, fp)