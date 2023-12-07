
from utilities import CommonVar
import datetime
import os
from flask import jsonify, redirect, render_template, request, session, url_for
from route.redirectPage import redirectPage
from tools.register import excel_to_json, singelReg
from utilities import jsonIO, utilities
import pandas as pd






def load(app):
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

            CommonVar.accountData = jsonIO.load_data('data/accountData.json')
            aRecords = jsonIO.load_data('data/academicRecordsData.json')
            courseCodeList = jsonIO.load_data('data/courseCodes.json')
            for AccountID in AccountIDs:
                for account in CommonVar.accountData:


                    if account["AccountID"] == str(AccountID):
                        for aRecord in aRecords:
                            
                            if aRecord["AccountID"] == str(AccountID):
                                if PostData['semester'] not in tuple(aRecord['general'].keys()):
                                    aRecord['general'][PostData['semester']] = []
                                if PostData['semester'] not in tuple(account["study"].keys()):
                                    account["study"][PostData['semester']] = []
                                if PostData['courseCode'] in account["study"][PostData['semester']]:
                                    break
                                aRecord['general'][PostData['semester']].append({
                                    "courseCode" : PostData['courseCode'],
                                    "courseName" : courseCodeList[PostData['courseCode']],
                                    "grade" : "-"
                                })
                        print(type(PostData['courseCode']))

                        if PostData['courseCode'] not in account["study"][PostData['semester']]:
                            account["study"][PostData['semester']].append(PostData['courseCode'])
                            print(account["study"])
                        break

            jsonIO.save_data(aRecords, 'data/academicRecordsData.json')
            jsonIO.save_data(CommonVar.accountData, 'data/accountData.json')
            CommonVar.accountData = jsonIO.load_data("data/accountData.json")
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
            CommonVar.accountData = jsonIO.load_data('data/accountData.json')

            for account in CommonVar.accountData:
                if account["AccountID"] == str(AccountID):
                    print(type(PostData['courseCode']))
                    if [PostData['semester']] not in tuple(account["teache"].keys()):
                        account["teache"][PostData['semester']] = []
                    if PostData['courseCode'] not in account["teache"][PostData['semester']]:
                        account["teache"][PostData['semester']].append(PostData['courseCode'])
                        print(account["teache"])
            jsonIO.save_data(CommonVar.accountData, 'data/accountData.json')
            CommonVar.accountData = jsonIO.load_data("data/accountData.json")
            return ""    
    @app.route("/course/create", methods = ['POST'])
    def courseCreate():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            form = request.form.to_dict()
            course = jsonIO.load_data('data\courseCodes.json')
            print(type(course))
            print(type(form))
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
                matchedAccDatas = [item for item in CommonVar.accountData if item["AccountID"].startswith(query) ]
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

                auth = jsonIO.load_data("data/auth.json")
                CommonVar.accountData = jsonIO.load_data("data/accountData.json")
                return redirectPage("/adminTool", f"Student {request.form.get('LastName')}{request.form.get('FirstName')}({request.form.get('AccountID')}) Registration successful")
            else:
                return redirectPage("/adminTool", "Account ID Repeated")
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

                auth = jsonIO.load_data("data/auth.json")
                CommonVar.accountData = jsonIO.load_data("data/accountData.json")
                return redirectPage("/adminTool", f"Teacher {request.form.get('LastName')}{request.form.get('FirstName')}({request.form.get('AccountID')}) Registration successful")
            else:
                return redirectPage("/adminTool", "Account ID Repeated")


    @app.route("/register/xlsx", methods= ['POST'])
    def xlsxRegister():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            file = request.files['file']
            if excel_to_json(file):

                auth = jsonIO.load_data("data/auth.json")
                CommonVar.accountData = jsonIO.load_data("data/accountData.json")
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
                data = [item for item in CommonVar.accountData if item["AccountID"] == session['username'] ][0]
                courseList = jsonIO.load_data("data\courseCodes.json")
                SemesterOptions = getSemesterOption()
                # SemesterOptions.reverse()
                return render_template('adminTool.html',accountData = data , queryData = CommonVar.accountData, courseList= courseList, SemesterOptions = SemesterOptions)

    @app.route("/GetAccountData")
    def GetAccountData():
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            return jsonify(CommonVar.accountData)
