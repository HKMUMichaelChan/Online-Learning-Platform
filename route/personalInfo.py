

import os
from flask import render_template, render_template_string, request, session
from werkzeug.utils import secure_filename
from utilities import jsonIO, utilities



def load(app, accountData):
    @app.route("/personal-info")
    @app.route("/personal-info/")
    def personal_info():
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return authError
        else:
                ###
            global accountData
            accountData = jsonIO.load_data("data/accountData.json")
            session['token'] = utilities.tokenAlive(app)
            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
            if os.path.exists("static/accountIcon/" + session['username'] + ".jpg"):
                icon_path = "/static/accountIcon/" + session['username'] + ".jpg"
            else:
                icon_path = "/static/accountIcon/default.jpg"
            return render_template('personal-info.html',accountData = data , AccRole = session['username'][0], role = session['username'][0], icon_path = icon_path)
            ###

    @app.route("/personal-info/<accountID>")
    def personal_info_adminVer(accountID):
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
                ###
                session['token'] = utilities.tokenAlive(app)
                data = [item for item in accountData if item["AccountID"] == accountID ][0]
                if os.path.exists("static/accountIcon/" + accountID + ".jpg"):
                    icon_path = "/static/accountIcon/" + accountID + ".jpg"
                else:
                    icon_path = "/static/accountIcon/default.jpg"

                return render_template('personal-info.html',accountData = data , AccRole = accountID[0], role = "3", icon_path = icon_path)
    
    @app.route("/upload", methods=['POST'])
    def upload():
        authError = utilities.authVerify(app, 1)


        if authError is not None:
            return authError
        else:
                session['token'] = utilities.tokenAlive(app)
                ###
                file = request.files['file']
                filename = secure_filename(file.filename)
                extension = filename.rsplit('.', 1)[1].lower()
                utilities.create_blank_file("static/accountIcon/" + session['username'] + ".jpg")
                closeScript = '''
                        <script>
                            function closeWindow() {
                                window.opener.location.reload()
                                window.close();
                                
                            }
                            closeWindow();
                        </script>
                    '''
                if extension == 'jpg' or extension == 'jpeg':

                    
                    file.save("static/accountIcon/" + session['username'] + ".jpg")

                    utilities.crop_to_square("static/accountIcon/" + session['username'] + ".jpg")

                    return render_template_string(closeScript)
                    # 文件是 JPG 類型
                elif extension == 'png':
                        
                    utilities.convert_png_to_jpg(file, "static/accountIcon/" + session['username'] + ".jpg")
                    utilities.crop_to_square("static/accountIcon/" + session['username'] + ".jpg")
                    # 文件是 PNG 類型
                    return render_template_string(closeScript)
                else:
                    # 其他類型的文件
                    pass


                data = [item for item in accountData if item["AccountID"] == session['username'] ][0]

                return render_template('home.html',accountData = data )
        
    @app.route("/editInfo/", methods= ['POST'])
    def editInfo():
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return authError
        else:
                global accountData
                data = [item for item in accountData if item["AccountID"] == session['username'] ][0]

                # decoded_text = unquote(request.get_data())

                # print(decoded_text)
                PostData :dict= request.json
                

                    
                accountData = jsonIO.load_data("data/accountData.json")
                accountID = session['username']
                for item in accountData:
                    if item["AccountID"] == accountID:
                        print("acc found")
                        # 在匹配的字典中进行更新
                        for key in PostData.keys():
                            for orginalKey in item.keys():
                                if key == orginalKey:
                                    print("key found")
                                    item[orginalKey] = PostData[key]
                jsonIO.save_data(accountData, "data/accountData.json")


                return render_template('home.html',accountData = data )

    @app.route("/editInfo/<AccountID>", methods= ['POST'])
    def editInfo_adminVer(AccountID):
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
                global accountData
                data = [item for item in accountData if item["AccountID"] == AccountID ][0]

                # decoded_text = unquote(request.get_data())

                # print(decoded_text)
                PostData :dict= request.json
                

                    
                accountData = jsonIO.load_data("data/accountData.json")

                for item in accountData:
                    if item["AccountID"] == AccountID:
                        print("acc found")
                        # 在匹配的字典中进行更新
                        for key in PostData.keys():
                            for orginalKey in item.keys():
                                if key == orginalKey:
                                    print("key found")
                                    item[orginalKey] = PostData[key]
                jsonIO.save_data(accountData, "data/accountData.json")


                return render_template('home.html',accountData = data )

    @app.route("/upload/<AccountID>", methods=['POST'])
    def upload_adminVer(AccountID):
        authError = utilities.authVerify(app, 3)


        if authError is not None:
            return authError
        else:
                session['token'] = utilities.tokenAlive(app)
                ###
                file = request.files['file']
                filename = secure_filename(file.filename)
                extension = filename.rsplit('.', 1)[1].lower()
                utilities.create_blank_file("static/accountIcon/" + AccountID + ".jpg")
                closeScript = '''
                        <script>
                            function closeWindow() {
                                window.opener.location.reload()
                                window.close();
                                
                            }
                            closeWindow();
                        </script>
                    '''
                if extension == 'jpg' or extension == 'jpeg':

                    
                    file.save("static/accountIcon/" + AccountID + ".jpg")

                    utilities.crop_to_square("static/accountIcon/" + AccountID + ".jpg")

                    return render_template_string(closeScript)
                    # 文件是 JPG 類型
                elif extension == 'png':
                        
                    utilities.convert_png_to_jpg(file, "static/accountIcon/" + AccountID + ".jpg")
                    utilities.crop_to_square("static/accountIcon/" + AccountID + ".jpg")
                    # 文件是 PNG 類型
                    return render_template_string(closeScript)
                else:
                    # 其他類型的文件
                    pass


                data = [item for item in accountData if item["AccountID"] == AccountID ][0]

                return render_template('home.html',accountData = data )
