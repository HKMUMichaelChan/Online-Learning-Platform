import pandas as pd
import json
from datetime import datetime
from werkzeug.security import generate_password_hash
from utilities import CommonVar, jsonIO

def singelReg(AccountID, LastName, FirstName, Sex, HKId,  Birthday, Address, PhoneNo, SpecialEducationalNeeds, Nationality):
    with open("data/auth.json", 'r') as file:
        data  = json.load(file)


    CommonVar.accountData = jsonIO.load_data("data/accountData.json")
    with open("data/academicRecordsData.json", 'r') as file:
        ARdata  = json.load(file)

    user = []
    for dat in data:
        user.append(dat['username'])



    if str(AccountID) not in user:
        password = HKId.replace("(","")
        password = password.replace(")","")
        hashed_password = generate_password_hash(password[:-2])
        data.append({
            'username': str(AccountID),
            'password': str(hashed_password)
        })
        CommonVar.accountData.append({
                'AccountID' : str(AccountID),
                'LastName' : LastName,
                'FirstName' : FirstName,
                'Sex': Sex,
                'HKID':HKId,
                'Birthday' : str(Birthday),
                'Address' : Address,
                'PhoneNo' : PhoneNo,
                'SpecialEducationalNeeds' : SpecialEducationalNeeds,
                'Nationality' : Nationality,
                "Email" : "/",
                "study" : {},
                "teache" : {}

        })
        print("已新增 " + str(AccountID))
        print("已新增 " + str(AccountID))
        ARdata.append({
                    "AccountID": str(AccountID),
                    "general":{

                    },
                    "others":[
                        
                    ]
        })
        with open("data/academicRecordsData.json", 'w') as ARfile:
            json.dump(ARdata, ARfile, indent=4)
        jsonIO.save_data(CommonVar.accountData, "data/accountData.json")
        with open("data/auth.json", 'w') as file:
            json.dump(data, file, indent=4)


       
        return True
    return False
def excel_to_json(file_path ):
    # 讀取Excel文件
    df = pd.read_excel(file_path, sheet_name=0)
    
    # 提取指定的兩列數據
    AccountIDs = df["AccountID"].tolist() # 用戶名列
    HKIds = df["HKID"].tolist()  # 密碼列
    lastnames = df["LastName"].tolist()
    firstnames = df["FirstName"].tolist()
    sexs = df["Sex"].tolist()
    birthdays = df["Birthday"].tolist()
    Addresss = df["Address"].tolist()
    PhoneNos = df["PhoneNo"].tolist()
    SpecialEducationalNeedss  = df["SpecialEducationalNeeds"].tolist()
    Nationalitys  = df["Nationality"].tolist()
  

    # 建立JSON數據
    with open("data/auth.json", 'r') as file:
        data  = json.load(file)

    with open("data/accountData.json", 'r') as file:
        CommonVar.accountData  = json.load(file)
        
    with open("data/academicRecordsData.json", 'r') as file:
        ARdata  = json.load(file)
    user = []
    for dat in data:
        user.append(dat['username'])
    with open("data/accountData.json", 'w') as Accountfile:
        with open("data/auth.json", 'w') as Authfile:
            with open("data/academicRecordsData.json", 'w') as ARfile:
            
                for AccountID, HKId ,lastname ,firstname, sex,birthday, Address, PhoneNo, SpecialEducationalNeeds, Nationality in zip(AccountIDs, HKIds ,lastnames ,firstnames, sexs, birthdays, Addresss, PhoneNos, SpecialEducationalNeedss, Nationalitys):
                    password = HKId.replace("(","")
                    password = password.replace(")","")
                    hashed_password = generate_password_hash(password[:-2])

                    if str(AccountID) not in user:
                        data.append({
                            'username': str(AccountID),
                            'password': str(hashed_password)
                        })
                        CommonVar.accountData.append({
                                'AccountID' : str(AccountID),
                                'LastName' : lastname,
                                'FirstName' : firstname,
                                'Sex': sex,
                                'HKID':HKId,
                                'Birthday' : str(birthday),
                                'Address' : Address,
                                'PhoneNo' : PhoneNo,
                                'SpecialEducationalNeeds' : SpecialEducationalNeeds,
                                'Nationality' : Nationality,
                                "Email" : "/",
                                "study" : {},
                                "teache" : {}
                        })
                        print("已新增 " + str(AccountID))
                        ARdata.append({
                                    "AccountID": str(AccountID),
                                    "general":{

                                    },
                                    "others":[
                                        
                                    ]
                        })

                json.dump(ARdata, ARfile, indent=4)
                json.dump(CommonVar.accountData, Accountfile, indent=4)
                
                json.dump(data, Authfile, indent=4)
    return True
        
    
