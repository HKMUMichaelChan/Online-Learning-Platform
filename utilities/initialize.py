import json
import os
from werkzeug.security import generate_password_hash

from utilities import CommonVar




def initialize():
    #需要的文件
    files = [
        "data/auth.json",
        "data/accountData.json",
        "data/academicRecordsData.json",
        "data/filesToUUIDs.json",
        "data/courseCodes.json"
    ]

    data = {}
    for file_name in files:
        if not os.path.exists(file_name):
            # 文件不存在，產生文件
            
            
            if file_name == files[0]:
                    CommonVar.initialize = True

            elif file_name == files[1]:
                accountData = []
                accountData.append({
                        'AccountID' : '30000000',
                        'LastName' : ' ',
                        'FirstName' : 'Administrator',
                        'HKID' : 'A123456(7)',
                        'Sex': '/',
                        'Birthday' : '/',
                        'Address' : '/',
                        'PhoneNo' : '/',
                        'SpecialEducationalNeeds' : '/',
                        'Nationality' : '/',
                        "Email": "test@email.com",
                        "study":
                            {
                                # "2023-Autumn":[
                                #     "course1",
                                #     "course2"
                                # ]
                            }

                        ,
                        "teache":
                            {
                                # "2024-Spring":[
                                #     "course1",
                                #     "course2"
                                # ]
                            }
                        
                })
                with open("data/accountData.json", 'w') as file:
                    json.dump(accountData, file, indent=4)
                    print(f"文件 '{file_name}' 已建立")

            elif file_name == files[2]:
                academicRecordsData = [
                    {
                        "AccountID": "30000000",
                        "general":{
                            # "2023-Autumn":[
                                # {
                                #     "courseCode" : "100",
                                #     "courseName" : "name",
                                #     "grade" : "A"
                                # },
                                # {
                                #     "courseCode" : "200",
                                #     "courseName" : "namawdwe",
                                #     "grade" : "B"
                                # }
                            ],
                            "2024-Spring":[
                                # {
                                #     "courseCode" : "course3",
                                #     "courseName" : "name",
                                #     "grade" : "C"
                                # },
                                # {
                                #     "courseCode" : "course4",
                                #     "courseName" : "name",
                                #     "grade" : "D"
                                # }
                            # ]
                        },
                        "others":[
                            {
                                "date":"2023/11/19",
                                "event":"nice competion",
                                "award":"No.1"
                            },
                            {
                                "date":"2023/11/22",
                                "event":"not good competion",
                                "award":"No.2"
                            }
                        ]

                    }
                ]

                with open("data/academicRecordsData.json", 'w') as file:
                    json.dump(academicRecordsData, file, indent=4)
                    print(f"文件 '{file_name}' 已建立")
            else:
                with open(file_name, 'w') as file:
                    json.dump({}, file, indent=4)
                    print(f"文件 '{file_name}' 已建立")
        else:
            print(f"文件 '{file_name}' 已存在。")

    