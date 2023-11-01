import pandas as pd
import json
from datetime import datetime
from werkzeug.security import generate_password_hash

def excel_to_json(file_path ):
    # 读取Excel文件
    df = pd.read_excel(file_path, sheet_name=0)
    
    # 提取指定的两列数据
    AccountIDs = df["AccountID"].tolist() # 用户名列
    HKIds = df["HKID"].tolist()  # 密码列
    lastnames = df["LastName"].tolist()
    firstnames = df["FirstName"].tolist()
    sexs = df["Sex"].tolist()
    birthdays = df["Birthday"].tolist()
    Addresss = df["Address"].tolist()
    PhoneNos = df["PhoneNo"].tolist()
    SpecialEducationalNeedss  = df["SpecialEducationalNeeds"].tolist()
    Nationalitys  = df["Nationality"].tolist()
  

    # 创建JSON数据
    with open("Online-Learning-Platform-Server-side/data/auth.json", 'r') as file:
        data  = json.load(file)

    with open("Online-Learning-Platform-Server-side/data/accountData.json", 'r') as file:
        accountData  = json.load(file)

    user = []
    for dat in data:
        user.append(dat['username'])
    
    for AccountID, HKId ,lastname ,firstname, sex,birthday, Address, PhoneNo, SpecialEducationalNeeds, Nationality in zip(AccountIDs, HKIds ,lastnames ,firstnames, sexs, birthdays, Addresss, PhoneNos, SpecialEducationalNeedss, Nationalitys):
        password = HKId.replace("(","")
        password = password.replace(")","")
        hashed_password = generate_password_hash(password[:-2])

        if str(AccountID) not in user:
            data.append({
                'username': str(AccountID),
                'password': str(hashed_password)
            })
            accountData.append({
                    'AccountID' : str(AccountID),
                    'LastName' : lastname,
                    'FirstName' : firstname,
                    'Sex': sex,
                    'Birthday' : str(birthday),
                    'Address' : Address,
                    'PhoneNo' : PhoneNo,
                    'SpecialEducationalNeeds' : SpecialEducationalNeeds,
                    'Nationality' : Nationality
            })
            print("已新增 " + str(AccountID))
            with open("Online-Learning-Platform-Server-side/data/accountData.json", 'w') as file:
                json.dump(accountData, file, indent=4)


    
    
    return data

# 示例使用
if __name__ == "__main__":
    file_path = "Online-Learning-Platform-Server-side/tools/accountData.xlsx"  # Excel文件路径

    
    
    
    json_data = excel_to_json(file_path)



    print(json_data)
    with open("Online-Learning-Platform-Server-side/data/auth.json", 'w') as file:
        json.dump(json_data, file, indent=4)