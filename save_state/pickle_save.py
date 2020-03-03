import json
def save_data_into_json(data, filename):
    json.dump(data, open(filename, 'w'))
def load_data_from_json(filename):
    return json.load(open(filename))