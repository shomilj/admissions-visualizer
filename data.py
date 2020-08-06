import json

def load_columns():
    columns = json.load(open('data/columns.json'))
    return columns