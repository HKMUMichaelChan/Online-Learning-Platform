import json
import os
from werkzeug.security import generate_password_hash





def initialize():
    #需要的文件
    files = [
        "data/auth.json",
        "data/accountData.json"

    ]

    data = {}
    for file_name in files:
        if not os.path.exists("Online-Learning-Platform/" + file_name):
            # 文件不存在，產生文件
            
            
            if file_name == files[0]:
                with open("Online-Learning-Platform/" + file_name, 'w') as file:
                    print(f"文件 '{file_name}' 不存在，正在初始化文件。請輸入初始管理員密碼：\n")
                    password = input("<Password of Administrator>")
                    hashed_password = generate_password_hash(password)
                    data = []
                    
                    data.append({
                        'username': '00000000',
                        'password': str(hashed_password)
                    })
                    print(f"密碼已設定，管理員用戶名為(8個0)'00000000'")

                    
                    json.dump(data, file)
            elif file_name == files[1]:
                accountData = []
                accountData.append({
                        'AccountID' : '00000000',
                        'LastName' : ' ',
                        'FirstName' : 'Administrator',
                        'HKID' : 'A123456(7)',
                        'Sex': '/',
                        'Birthday' : '/',
                        'Address' : '/',
                        'PhoneNo' : '/',
                        'SpecialEducationalNeeds' : '/',
                        'Nationality' : '/'
                })
                with open("Online-Learning-Platform/data/accountData.json", 'w') as file:
                    json.dump(accountData, file, indent=4)
        else:
            print(f"文件 '{file_name}' 已存在。")

    