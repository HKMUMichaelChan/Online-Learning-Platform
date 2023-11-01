import pandas as pd
import random
from datetime import datetime

# 產生學生列表數據
students = [
    {
        'AccountID': '12345678',
        'LastName': 'Smith',
        'FirstName': 'John',
        'HKID': 'A123456(7)',
        'Sex': 'Male',
        'Birthday': datetime(2005, 5, 10),
        'Address': '123 Main St, Hong Kong',
        'PhoneNo': '12345678',
        'SpecialEducationalNeeds': "NA",
        'Nationality': 'Hong Kong'
    },
    {
        'AccountID': '12345679',
        'LastName': 'Johnson',
        'FirstName': 'Emma',
        'HKID': 'A123456(7)',
        'Sex': 'Female',
        'Birthday': datetime(2006, 8, 15),
        'Address': '456 Elm St, Hong Kong',
        'PhoneNo': '98765432',
        'SpecialEducationalNeeds': "need1, \n need2",
        'Nationality': 'Hong Kong'
    },
    # 添加更多学生信息...
]

# 建立 Excel 文件
excel_file = 'Online-Learning-Platform/tools/accountData.xlsx'
writer = pd.ExcelWriter(excel_file)

# 建立資料框
data = pd.DataFrame(students)

# 調整列的順序
columns_order = ['AccountID', 'LastName', 'FirstName', 'HKID', 'Sex', 'Birthday', 'Address', 'PhoneNo', 'SpecialEducationalNeeds', 'Nationality']
data = data[columns_order]

# 將資料寫入工作表
data.to_excel(writer, index=False)

# 儲存 Excel 文件
writer._save()

print("學生清單試算表已產生並儲存。")