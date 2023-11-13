

import datetime
import os
from flask import jsonify, redirect, render_template, request, session, url_for
from route.redirectPage import redirectPage
from tools.register import excel_to_json, singelReg
from utilities import jsonIO, utilities
import pandas as pd






def load(app, accountData):
    @app.route("/course/registration/student", methods = ['POST'])
    def courseReg():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            file = request.files['file']
            PostData :dict= request.form.to_dict()


            df = pd.read_excel(file, sheet_name=0)
            AccountIDs = df["AccountID"].tolist()

            accountData = jsonIO.load_data('data/accountData.json')
            for AccountID in AccountIDs:
                for account in accountData:
                    if account["AccountID"] == str(AccountID):
                        print(type(PostData['courseCode']))
                        if [PostData['semester']] not in tuple(account["study"].keys()):
                            account["study"][PostData['semester']] = []
                        if PostData['courseCode'] not in account["study"][PostData['semester']]:
                            account["study"][PostData['semester']].append(PostData['courseCode'])
                            print(account["study"])
            jsonIO.save_data(accountData, 'data/accountData.json')
            return ""

    @app.route("/course/registration/teacher", methods = ['POST'])  
    def courseRegTeacher():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:

            PostData :dict= request.form.to_dict()



            AccountID = str(PostData['AccountID'])
            print(AccountID)
            accountData = jsonIO.load_data('data/accountData.json')

            for account in accountData:
                if account["AccountID"] == str(AccountID):
                    print(type(PostData['courseCode']))
                    if [PostData['semester']] not in tuple(account["teache"].keys()):
                        account["teache"][PostData['semester']] = []
                    if PostData['courseCode'] not in account["teache"][PostData['semester']]:
                        account["teache"][PostData['semester']].append(PostData['courseCode'])
                        print(account["teache"])
            jsonIO.save_data(accountData, 'data/accountData.json')
            accountData = jsonIO.load_data("data/accountData.json")
            return ""    
    @app.route("/course/create", methods = ['POST'])
    def courseCreate():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            form = request.form.to_dict()
            course = jsonIO.load_data('data\courseCodes.json')
            course[form['courseCode']] = form['courseName']
            jsonIO.save_data(course, 'data\courseCodes.json')
            return redirect(url_for('adminTool'))
        
    @app.route("/course/add", methods = ['POST'])
    def courseAdd():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            form = request.form.to_dict()
            if not os.path.exists(f"data\course\{form['semester']}\{form['courseCode']}") :
                os.makedirs(f"data\course\{form['semester']}\{form['courseCode']}/files")
                os.makedirs(f"data\course\{form['semester']}\{form['courseCode']}/submitions")
                jsonIO.createDict(f"data\course\{form['semester']}\{form['courseCode']}/data.json")
                data = {    
                    "announcements": [],
                    "resourses": [],
                    "assignments": []
                            }
                jsonIO.save_data(data, f"data\course\{form['semester']}\{form['courseCode']}/data.json")
                return ""
            else:
                return ""

    @app.route("/IDQuery", methods= ['POST'])
    def query_json():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            if request.method == 'POST':
                query = request.form.get('query')

                # 这里替换为你的 JSON 文件路径

                matches = []
                matchedAccDatas = [item for item in accountData if item["AccountID"].startswith(query) ]
                for matchedAccData in matchedAccDatas:

                    matches.append(matchedAccData['AccountID'])

                return matches


    @app.route("/register/student", methods= ['POST'])
    def studentRegister():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            if singelReg(request.form.get('AccountID'),
                    request.form.get('LastName'),
                    request.form.get('FirstName'),
                    request.form.get('Sex'),
                    request.form.get('HKId'),
                    request.form.get('Birthday'),
                    request.form.get('Address'),
                    request.form.get('PhoneNo'),
                    request.form.get('SpecialEducationalNeeds'),
                    request.form.get('Nationality')
                    ):
                global auth, accountData
                auth = jsonIO.load_data("data/auth.json")
                accountData = jsonIO.load_data("data/accountData.json")
                return redirectPage("/adminTool", f"學生 {request.form.get('LastName')}{request.form.get('FirstName')}({request.form.get('AccountID')}) 注冊成功")
            else:
                return redirectPage("/adminTool", f"資料不正確")
        # return '<script>alert("提交成功！"); window.location.href="/";</script>'


    @app.route("/register/teacher", methods= ['POST'])
    def teacherRegister():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            if  singelReg(request.form.get('AccountID'),
                    request.form.get('LastName'),
                    request.form.get('FirstName'),
                    request.form.get('Sex'),
                    request.form.get('HKId'),
                    request.form.get('Birthday'),
                    request.form.get('Address'),
                    request.form.get('PhoneNo'),
                    request.form.get('SpecialEducationalNeeds'),
                    request.form.get('Nationality')
                    ):
                global auth, accountData
                auth = jsonIO.load_data("data/auth.json")
                accountData = jsonIO.load_data("data/accountData.json")
                return redirectPage("/adminTool", f"教師 {request.form.get('LastName')}{request.form.get('FirstName')}({request.form.get('AccountID')}) 注冊成功")
            else:
                return redirectPage("/adminTool", "Account ID 已重複")


    @app.route("/register/xlsx", methods= ['POST'])
    def xlsxRegister():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            file = request.files['file']
            if excel_to_json(file):
                global auth, accountData
                auth = jsonIO.load_data("data/auth.json")
                accountData = jsonIO.load_data("data/accountData.json")
                return redirectPage("/adminTool", f"注冊成功")
            else:
                return redirectPage("/adminTool", "Account ID 已重複")
            
    def getSemesterOption():
        current_month = datetime.datetime.now().month
        year = current_year = datetime.datetime.now().year
        current_season = get_season(current_month)
        semesterOption = []

        for _ in range(3):
            semesterOption.append(f"{year}-{current_season}")
            current_season, year = get_next_season(current_season, year)
            

        return semesterOption

    def get_season(month):
        if month in (1, 2, 3, 4):
            return 'Spring'
        elif month in (5, 6, 7, 8):
            return 'Summer'
        elif month in (9, 10, 11, 12):
            return 'Autumn'

    def get_next_season(season, year):
        if season == 'Spring':
            return 'Summer', year
        elif season == 'Summer':
            return 'Autumn', year
        elif season == 'Autumn':
            return 'Spring', year + 1

    @app.route("/adminTool")
    def adminTool():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
                data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
                courseList = jsonIO.load_data("data\courseCodes.json")
                SemesterOptions = getSemesterOption()
                # SemesterOptions.reverse()
                return render_template('adminTool.html',accountData = data , queryData = accountData, courseList= courseList, SemesterOptions = SemesterOptions)

    @app.route("/GetAccountData")
    def GetAccountData():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            return jsonify(accountData)
