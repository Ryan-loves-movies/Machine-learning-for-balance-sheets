from save_state.pickle_save import load_data_from_json, save_data_into_json


# Dates: to see the number of stocks with sufficient historical data
dates = {}
balance_sheets = load_data_from_json("balance_sheets/filtered_balance_sheets.json")

for symb in balance_sheets:
    balance_sheet = balance_sheets[symb]
    no_of_dates = []
    for year in balance_sheet['financials']:
        no_of_dates.append(year['date'])
    dates[symb] = no_of_dates

dates_no = {i:len(dates[i]) for i in dates}

# Just seeing the distribution of data with enough data points
# print(dates_no)
# itera = 2020
# no = 0
# too_young = 0
# total = 0

# while itera>2000:
#     sum = 0
#     for i in dates_no:
#         if dates_no[i] == no:
#             sum+=1
#     print(f'Number of stocks that started in year {str(itera)} is: {str(sum)}')
#     if itera > 2012:
#         too_young += sum
#     total += sum
#     itera -= 1
#     no+=1

to_data = []
for i in dates_no:
    if dates_no[i]>7:
        to_data.append(i)

print(to_data)
print(len(to_data))
print(too_young)
print(total)
