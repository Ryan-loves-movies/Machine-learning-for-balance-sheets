from save_state.pickle_save import save_data_into_json, load_data_from_json
balance_sheets = load_data_from_json('balance_sheets/full_balance_sheet_list.json')
filtered_dict = { i : balance_sheets[i] for i in balance_sheets if balance_sheets[i]!={}}
print(len(filtered_dict))
save_data_into_json(filtered_dict, 'filtered_balance_sheets.json')