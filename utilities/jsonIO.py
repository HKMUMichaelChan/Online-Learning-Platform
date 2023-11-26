import json



def load_data(file_name):
    try:
        with open(file_name, 'r' ,encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return []


def save_data(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def createDict(path):
    with open(path, 'w') as file:
        json.dump({}, file, indent=4)

