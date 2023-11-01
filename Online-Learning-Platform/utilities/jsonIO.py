import json

# 讀取JSON文件
def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return []

# 儲存資料到JSON文件
def save_data(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file)

# 新增記錄
def add_record(data, record):
    data.append(record)

# 根據條件查詢記錄
def query_records(data, condition):
    results = []
    for record in data:
        if condition(record):
            results.append(record)
    return results