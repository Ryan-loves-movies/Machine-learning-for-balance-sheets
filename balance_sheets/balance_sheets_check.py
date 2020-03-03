from pickle_save import load_data_from_json
from all_stock_symb import all_stocks
print(len(all_stocks))
print(len(load_data_from_json('full_balance_sheet_list.json')))