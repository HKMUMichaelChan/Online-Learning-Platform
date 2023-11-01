import pandas as pd
import random
from datetime import datetime

# 生成学生列表数据
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

# 创建 Excel 文件
excel_file = 'Online-Learning-Platform/tools/accountData.xlsx'
writer = pd.ExcelWriter(excel_file)

# 创建数据框
data = pd.DataFrame(students)

# 调整列的顺序
columns_order = ['AccountID', 'LastName', 'FirstName', 'HKID', 'Sex', 'Birthday', 'Address', 'PhoneNo', 'SpecialEducationalNeeds', 'Nationality']
data = data[columns_order]

# 将数据写入工作表
data.to_excel(writer, index=False)

# 保存 Excel 文件
writer._save()

print("学生列表试算表已生成并保存。")