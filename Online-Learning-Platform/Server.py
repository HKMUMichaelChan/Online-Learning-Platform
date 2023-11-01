from datetime import datetime, timedelta
import os
from flask import Flask, render_template_string, request, render_template, redirect, url_for , session
import jwt
from werkzeug.security import check_password_hash
import utilities.jsonIO as jsonIO
from utilities.initialize import initialize
from werkzeug.utils import secure_filename
from utilities.tojpg import convert_png_to_jpg
from tools.register import excel_to_json, singelReg
app = Flask(__name__)

# 系統亂數種子
app.secret_key = 'your_secret_keya'

def redirectPage(target, message):
    session['target'] = target
    session['message'] = message
    if target == "/login":
        return render_template('transition.html', target="/login", message = message)
    elif target == "/logout":
        return render_template('transition.html', target="/login", message = "賬號已登出")
    elif target == "/adminTool":
        return render_template('transition.html', target="/adminTool", message = message)
    else:
        return redirect(url_for('home'))
    
def authVerify():
    if 'token' in session:
        try:
            token = session['token']
            # 驗證令牌是否過期
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                return redirectPage("/login", "令牌已過期，請重新登入！！")

            return None #No Error
        except jwt.ExpiredSignatureError:
            return redirectPage("/login", "令牌已過期，請重新登入！！")
        except jwt.InvalidTokenError:
            return redirectPage("/login", "無效令牌，請重新登入！")    
    else:
        return redirectPage("/login", "未登入，請登入")  

@app.route("/register/student", methods= ['POST'])
def studentRegister():
    authError = authVerify()
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
            auth = jsonIO.load_data("Online-Learning-Platform/data/auth.json")
            accountData = jsonIO.load_data("Online-Learning-Platform/data/accountData.json")
            return redirectPage("/adminTool", f"學生 {request.form.get('LastName')}{request.form.get('FirstName')}({request.form.get('AccountID')}) 注冊成功")
        else:
            return redirectPage("/adminTool", f"資料不正確")
    # return '<script>alert("提交成功！"); window.location.href="/";</script>'


@app.route("/register/teacher", methods= ['POST'])
def teacherRegister():
    authError = authVerify()
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
            auth = jsonIO.load_data("Online-Learning-Platform/data/auth.json")
            accountData = jsonIO.load_data("Online-Learning-Platform/data/accountData.json")
            return redirectPage("/adminTool", f"教師 {request.form.get('LastName')}{request.form.get('FirstName')}({request.form.get('AccountID')}) 注冊成功")
        else:
            return redirectPage("/adminTool", "Account ID 已重複")


@app.route("/register/xlsx", methods= ['POST'])
def xlsxRegister():
    authError = authVerify()
    if authError is not None:
        return authError
    else:
        file = request.files['file']
        if excel_to_json(file):
            global auth, accountData
            auth = jsonIO.load_data("Online-Learning-Platform/data/auth.json")
            accountData = jsonIO.load_data("Online-Learning-Platform/data/accountData.json")
            return redirectPage("/adminTool", f"注冊成功")
        else:
            return redirectPage("/adminTool", "Account ID 已重複")
@app.route("/adminTool")
def adminTool():
    authError = authVerify()
    if authError is not None:
        return authError
    else:
            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
            return render_template('adminTool.html',accountData = data )



@app.route("/academicRecords")
def academicRecords():
    authError = authVerify()
    if authError is not None:
        return authError
    else:
            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
            return render_template('academicRecords.html',accountData = data )


@app.route("/editInfo", methods= ['POST'])
def editInfo():
    authError = authVerify()
    if authError is not None:
        return authError
    else:
            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]

            return render_template('home.html',accountData = data )
            ###


@app.route("/upload", methods=['POST'])
def upload():
    authError = authVerify()
    if authError is not None:
        return authError
    else:
            ###
            file = request.files['file']
            filename = secure_filename(file.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            if not os.path.exists("Online-Learning-Platform/static/accountIcon/" + session['username'] + ".jpg"):
                with open("Online-Learning-Platform/static/accountIcon/" + session['username'] + ".jpg",'w') as file:
                    pass
            if extension == 'jpg' or extension == 'jpeg':

                    
                file.save("Online-Learning-Platform/static/accountIcon/" + session['username'] + ".jpg")
                return render_template_string('''
                    <script>
                        function closeWindow() {
                            window.opener.location.reload()
                            window.close();
                            
                        }
                        closeWindow();
                    </script>
                ''')
                # 文件是 JPG 類型
            elif extension == 'png':
                    
                convert_png_to_jpg(file, "Online-Learning-Platform/static/accountIcon/" + session['username'] + ".jpg")
                # 文件是 PNG 類型
                return render_template_string('''
                    <script>
                        function closeWindow() {
                            window.opener.location.reload()
                            window.close();
                            
                        }
                        closeWindow();
                    </script>
                ''')
            else:
                # 其他類型的文件
                pass


            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]

            return render_template('home.html',accountData = data )
            ###





@app.route("/home")
def home():
    authError = authVerify()
    if authError is not None:
        return authError
    else:
        data = [item for item in accountData if item["AccountID"] == session['username'] ][0]

        return render_template('home.html',accountData = data, role = session['username'][0] )



@app.route("/personal-info")
def personal_info():
    authError = authVerify()
    if authError is not None:
        return authError
    else:
            ###

            
        data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
        if os.path.exists("Online-Learning-Platform/static/accountIcon/" + session['username'] + ".jpg"):
            icon_path = "/static/accountIcon/" + session['username'] + ".jpg"
        else:
            icon_path = "/static/accountIcon/00000000.jpg"

        return render_template('personal-info.html',accountData = data , role = session['username'][0], icon_path = icon_path)
        ###



@app.route("/")
def index():
    authError = authVerify()
    if authError is not None:
        return authError
    else:


            return redirect(url_for('home'))
        


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 檢查使用者名稱是否存在
        if username not in users:
            return redirectPage("/login", "該用戶名稱不存在，請聯係IT人員協助。")

        # 檢查密碼是否匹配
        for dat in auth:
            if dat['username'] == username:
                hash = dat['password']

        if not check_password_hash(hash, password):
            return redirectPage("/login", "密碼錯誤，請重新輸入。\n如忘記密碼，請聯係IT人員協助。")

        session['username'] = username
        # 產生 JWT 令牌並設定過期時間為 30 分鐘
        expiration_time = datetime.utcnow() + timedelta(minutes=30)
        payload = {
            'username': username,
            'exp': expiration_time
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        session['token'] = token  # 將令牌儲存在 cookies 的 session 中
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirectPage("/logout", None)

if __name__ == "__main__":
    # 檢查系統是否已經初始化
    initialize()
    global auth, accountData
    auth = jsonIO.load_data("Online-Learning-Platform/data/auth.json")
    accountData = jsonIO.load_data("Online-Learning-Platform/data/accountData.json")
    users = []
    
    for dat in auth:
        users.append(dat['username'])
    app.run(host= '0.0.0.0' ,port=5000)