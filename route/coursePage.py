

import os
import time
import uuid
from flask import jsonify, redirect, render_template, request, send_file, session, url_for
from route.redirectPage import redirectPage
from utilities import jsonIO, utilities
from markupsafe import Markup



def load(app, accountData):

    
    @app.route("/course/")
    def courseIndex():
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return authError
        else:
            accountData = jsonIO.load_data("data/accountData.json")
            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
            if session['username'][0] == '1':
                mode = "study"
            elif session['username'][0] == '2':
                mode = "teache"
            else:
                mode = "study" ##admin
            
            
            semesters :dict = data[mode]
            print(semesters.keys())
            courseCodeToName = {}
            courseCodesJson = jsonIO.load_data("data/courseCodes.json")
            for semester in semesters.keys():
                for key in data[mode][semester]:
                    courseCodeToName[key] = courseCodesJson[key]
            preloadData = {
                "semesters": semesters.keys(),
                "courseCodeToName": courseCodeToName
            }
            
            return render_template("courseIndex.html", accountData = data, PreloadData = preloadData)
    
    @app.route("/course/<Semester>/<CourseCode>/assignmentForm")
    def createAssignmentForm(Semester,CourseCode):
        authError = utilities.authVerify(app, 2)
        if authError is not None:
            return authError
        else:
            if request.args.get("r") == '0':
                message = "已發佈作業，三秒後關閉視窗"
                return render_template("createAssignmentForm.html", Semester = Semester , CourseCode = CourseCode, message = message)
            else:
                message = ""
                return render_template("createAssignmentForm.html", Semester = Semester , CourseCode = CourseCode, message = message)

    @app.route("/course/<Semester>/<CourseCode>/assignment/create" , methods=['POST'])
    def createAssignment(Semester,CourseCode):
        authError = utilities.authVerify(app, 2)
        if authError is not None:
            return authError
        else:


            session['token'] = utilities.tokenAlive(app)
            files = request.files.getlist('file')
            PostData :dict= request.form.to_dict()
            PostData['files']=[]
            for file in files:
                
            # 生成唯一的文件名
                unique_uuid = str(uuid.uuid4())
                # '_' = filename 
                _, extension = os.path.splitext(file.filename)

                new_filename = unique_uuid + extension

                PostData['files'].append(new_filename)

                file.save("data\course/"+ Semester+ "/" +CourseCode + "/files/"+  "/" + new_filename)
                
                filesToUUIDs = jsonIO.load_data("data/filesToUUIDs.json")
                filesToUUIDs[unique_uuid] = file.filename
                jsonIO.save_data(filesToUUIDs,"data/filesToUUIDs.json")

            courseResourse = jsonIO.load_data(f"data/course/{Semester}/{CourseCode}/data.json")
            
            

            print(PostData)

            courseResourse['assignments'].append(PostData)

            jsonIO.save_data(courseResourse , f"data/course/{Semester}/{CourseCode}/data.json")
            return redirect(url_for('createAssignmentForm', Semester = Semester, CourseCode = CourseCode , r = 0))

    @app.route("/course/<Semester>/<CourseCode>/resourses/")
    def createResourseForm(Semester,CourseCode):
        authError = utilities.authVerify(app, 2)
        if authError is not None:
            return authError
        else:
            if request.args.get("r") == '0':
                message = "已發佈公告，三秒後關閉視窗"
                return render_template("createResourseForm.html", Semester = Semester , CourseCode = CourseCode, message = message)
            else:
                message = ""
                return render_template("createResourseForm.html", Semester = Semester , CourseCode = CourseCode, message = message)

    @app.route("/course/<Semester>/<CourseCode>/resourses/create" , methods=['POST'])
    def createResourse(Semester,CourseCode):
        authError = utilities.authVerify(app, 2)
        if authError is not None:
            return authError
        else:


            session['token'] = utilities.tokenAlive(app)
            files = request.files.getlist('file')
            PostData :dict= request.form.to_dict()
            PostData['files']=[]
            for file in files:
                
            # 生成唯一的文件名
                unique_uuid = str(uuid.uuid4())
                # '_' = filename 
                _, extension = os.path.splitext(file.filename)

                new_filename = unique_uuid + extension

                PostData['files'].append(new_filename)

                file.save("data\course/"+ Semester+ "/" +CourseCode + "/files/"+  "/" + new_filename)
                
                filesToUUIDs = jsonIO.load_data("data/filesToUUIDs.json")
                filesToUUIDs[unique_uuid] = file.filename
                jsonIO.save_data(filesToUUIDs,"data/filesToUUIDs.json")

            courseResourse = jsonIO.load_data(f"data/course/{Semester}/{CourseCode}/data.json")
            
            

            print(PostData)

            courseResourse['resourses'].append(PostData)

            jsonIO.save_data(courseResourse , f"data/course/{Semester}/{CourseCode}/data.json")
            return redirect(url_for('createResourseForm', Semester = Semester, CourseCode = CourseCode , r = 0))
        
    @app.route("/course/<Semester>/<CourseCode>/resourse/rm/<index>")
    def removeResourse(Semester, CourseCode, index):
        authError = utilities.authVerify(app, 2)
        

        if authError is not None:
            return authError
        else:
            print(int(index))
            courseResourse = jsonIO.load_data(f"data/course/{Semester}/{CourseCode}/data.json")
            for Resourse in courseResourse['resourses']:
                
                if Resourse['files'] != []:
                    for file in Resourse['files']:
                        os.remove("data/course/2023-Autumn/100/files/" + file)
            courseResourse['resourses'].pop(int(index))
            jsonIO.save_data(courseResourse , f"data/course/{Semester}/{CourseCode}/data.json")

            return ""    
            
    @app.route("/course/<Semester>/<CourseCode>/announcement")
    # @app.route("/course/<Semester>/<CourseCode>/announcement?message=<message>")
    def createAnnouncementForm(Semester,CourseCode):
        authError = utilities.authVerify(app, 2)
        if authError is not None:
            return authError
        else:
            if request.args.get("r") == '0':
                message = "已發佈公告，三秒後關閉視窗"
                return render_template("createAnnouncementsForm.html", Semester = Semester , CourseCode = CourseCode, message = message)
            else:
                message = ""
                return render_template("createAnnouncementsForm.html", Semester = Semester , CourseCode = CourseCode, message = message)
                
        
    @app.route("/course/<Semester>/<CourseCode>/announcement/create", methods = ["POST"])
    def createAnnouncement(Semester,CourseCode):
        authError = utilities.authVerify(app, 2)
        

        if authError is not None:
            return authError
        else:
            courseAnnouncement = jsonIO.load_data(f"data/course/{Semester}/{CourseCode}/data.json")
            PostData :dict= request.form.to_dict()
            print(PostData)
            courseAnnouncement['announcements'].append(PostData)
            jsonIO.save_data(courseAnnouncement , f"data/course/{Semester}/{CourseCode}/data.json")
            return redirect(url_for('createAnnouncementForm', Semester = Semester, CourseCode = CourseCode , r = 0))
        
    @app.route("/course/<Semester>/<CourseCode>/announcement/rm/<index>")
    def removeAnnouncement(Semester, CourseCode, index):
        authError = utilities.authVerify(app, 2)
        

        if authError is not None:
            return authError
        else:
            print(int(index))
            courseAnnouncement = jsonIO.load_data(f"data/course/{Semester}/{CourseCode}/data.json")
            courseAnnouncement['announcements'].pop(int(index))
            try:
                jsonIO.save_data(courseAnnouncement , f"data/course/{Semester}/{CourseCode}/data.json")
            except Exception as err:
                print(err)
            finally:
               return ""

            
    @app.route("/course/<Semester>/<CourseCode>/assignment")
    def assignment(Semester,CourseCode):
        authError = utilities.authVerify(app, 2)
        if authError is not None:
            return authError
        else:        
            folderPath = f"data/course/{Semester}/{CourseCode}/submitions/{session['username']}"
            filesPaths = os.listdir(folderPath)
            filesToUUIDs = jsonIO.load_data("data/filesToUUIDs.json")
            filesName = []
            for fileUUIDnExt in filesPaths:
                # '_' is extension
                fileUUID, _ = os.path.splitext(fileUUIDnExt)
                
                filesName.append(filesToUUIDs[fileUUID])
            PreloadData = {
                    "semester" : Semester,
                    "courseCode" : CourseCode,
                    "files" :[
                        filesName,
                        filesPaths
                    ]
                }
            return render_template("assignmentSubmitionForm.html", PreloadData = PreloadData)
        
    @app.route("/course/<Semester>/<CourseCode>/assignment/rm/<index>")
    def removeAssignment(Semester, CourseCode, index):
        authError = utilities.authVerify(app, 2)
        

        if authError is not None:
            return authError
        else:
            print(int(index))
            courseAssignment = jsonIO.load_data(f"data/course/{Semester}/{CourseCode}/data.json")
            for Assignment in courseAssignment['assignments']:
                
                if Assignment['files'] != []:
                    for file in Assignment['files']:
                        os.remove("data/course/2023-Autumn/100/files/" + file)
            courseAssignment['assignments'].pop(int(index))
            try:
                jsonIO.save_data(courseAssignment , f"data/course/{Semester}/{CourseCode}/data.json")
            except Exception as err:
                print(err)
            finally:
               return ""
            



    @app.route("/course/<Semester>/<CourseCode>/files/<fileName>")
    def downloadResourse(Semester,CourseCode, fileName):
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return authError
        else:
            session['token'] = utilities.tokenAlive(app)
            
            UUIDs = jsonIO.load_data("data/filesToUUIDs.json")
            for UUIDKey in UUIDs.keys():

                if UUIDs[UUIDKey] == fileName:
                    
                    _, ext = os.path.splitext(UUIDs[UUIDKey])
                    fileName = UUIDKey + ext

                    filePath = f"data/course/{Semester}/{CourseCode}/files/{fileName}"
                    return send_file(filePath, download_name= UUIDs[UUIDKey], as_attachment=True)

    @app.route("/course/<Semester>/<CourseCode>/view")
    def submitionView(Semester,CourseCode):
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return authError
        else:
            session['token'] = utilities.tokenAlive(app)
            folderPath = f"data/course/{Semester}/{CourseCode}/submitions/{session['username']}"
            filesPaths = os.listdir(folderPath)
            filesToUUIDs = jsonIO.load_data("data/filesToUUIDs.json")
            filesName = []
            for fileUUIDnExt in filesPaths:
                # '_' is extension
                fileUUID, _ = os.path.splitext(fileUUIDnExt)
                
                filesName.append(filesToUUIDs[fileUUID])
            print(filesName)
            UUIDsnNames = [
                filesName,
                filesPaths
            ]
            return jsonify(UUIDsnNames)

    @app.route("/course/<Semester>/<CourseCode>/assignment/submit",  methods=['POST'])
    def submitAssignment(Semester,CourseCode):
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return authError
        else:
            session['token'] = utilities.tokenAlive(app)
            files = request.files.getlist('file')
            for file in files:
            # 生成唯一的文件名
                unique_uuid = str(uuid.uuid4())
                # '_' = filename 
                _, extension = os.path.splitext(file.filename)

                new_filename = unique_uuid + extension


                file.save("data\course/"+ Semester+ "/" +CourseCode + "\submitions/"+ session['username'] + "/" + new_filename)
                
                filesToUUIDs = jsonIO.load_data("data/filesToUUIDs.json")
                filesToUUIDs[unique_uuid] = file.filename
                jsonIO.save_data(filesToUUIDs,"data/filesToUUIDs.json")

            closeScript = '''
                    <script>
                        function closeWindow() {
                            window.close();
                            
                        }
                        closeWindow();
                    </script>
                '''   
            return redirect('/course/' + Semester + '/' + CourseCode + '/assignment')

    @app.route("/course/<Semester>/<CourseCode>/rm/<filePath>",methods=['POST'])
    def submitionRm(Semester,CourseCode,filePath):
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return authError
        else:
            session['token'] = utilities.tokenAlive(app)
            

            folderPath = f"data/course/{Semester}/{CourseCode}/submitions/{session['username']}/"
            try:
                os.remove(folderPath + filePath)
            except FileNotFoundError:
                print("[ingored] FileNotFound")
            print(folderPath + filePath)
            return ""

    @app.route("/course/<Semester>/<CourseCode>/score")
    def scoreManagement(Semester,CourseCode):
        authError = utilities.authVerify(app, 2)
        if authError is not None:
            return authError
        else:  
            PreloadData = []
            js = jsonIO.load_data("data/academicRecordsData.json")
            accountData = jsonIO.load_data("data/accountData.json")
            for singleAccount in accountData:
                if Semester in singleAccount["study"].keys():

                    if CourseCode in singleAccount["study"][Semester]:
                        
                        for AccountRecords in js:
                            if  AccountRecords['AccountID'] == singleAccount['AccountID']:


                                for course in AccountRecords['general'][Semester]:
                                    if course['courseCode'] == CourseCode:
                                        PreloadData.append({
                                            "AccountID ": singleAccount['AccountID'],
                                            "FullName" : singleAccount['LastName'] + singleAccount['FirstName'],
                                            "Score" : course['grade']
                                        })


            

            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
            return render_template('scoreManagement.html',accountData = data, PreloadData = PreloadData)



    #course/2023-Autumn/100
    @app.route("/course/<Semester>/<CourseCode>")
    def coursePage(Semester,CourseCode):
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return authError
        else:
            #check if vaild Semester + CourseCode
            if not os.path.exists(f"data/course/{Semester}/{CourseCode}"):
                redirectPage("/home","Counld not found the Page")
            else:
                session['token'] = utilities.tokenAlive(app)
                data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
                CourseData = jsonIO.load_data(f"data/course/{Semester}/{CourseCode}/data.json")
                CourseName = jsonIO.load_data("data\courseCodes.json")[CourseCode]
                uuidData = jsonIO.load_data("data/filesToUUIDs.json")
                announcements = []
                for announcement in CourseData['announcements']:

                    
                    escapeTitle = Markup(announcement['title'])
                    escapeContent = Markup(announcement['content'])
                    announcement['title'] = escapeTitle
                    announcement['content'] = escapeContent

                    # print(announcement['content'])
                    announcements.append(announcement)


                assignments = []
                for assignment in CourseData['assignments']:

                    fileUUIDs = assignment['files']
                    fileNames = []
                    for fileUUID in fileUUIDs:
                        fileUUID, _ = os.path.splitext(fileUUID)
                        fileName = uuidData[fileUUID]
                        fileNames.append(fileName)
                    assignment['files'] = fileNames
                    assignments.append(assignment)

                resourses = []
                
                for resourse in CourseData['resourses']:
                    fileUUIDs = resourse['files']
                    fileNames = []
                    for fileUUID in fileUUIDs:
                        fileUUID, _ = os.path.splitext(fileUUID)
                        fileName = uuidData[fileUUID]
                        fileNames.append(fileName)
                    resourse['files'] = fileNames
                    resourses.append(resourse)
                PreloadData = {
                    "semester" : Semester,
                    "courseCode" : CourseCode,
                    "courseName" : CourseName,
                    "announcements" : announcements,
                    "assignments" : assignments,
                    "resourses" : resourses
                }
                

                return render_template('coursePage.html',accountData = data, PreloadData = PreloadData)
