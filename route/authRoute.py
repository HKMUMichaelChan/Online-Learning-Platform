import json
from utilities import CommonVar
from datetime import datetime, timedelta
import jwt
from werkzeug.security import check_password_hash
from flask import redirect, render_template, request, session, url_for
from route.redirectPage import redirectPage
from utilities import jsonIO, utilities
from werkzeug.security import generate_password_hash


def load(app):
    @app.route("/")
    def index():
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return redirect(url_for('login'))
        else:


            return redirect(url_for('home'))
        
    @app.route("/home")
    def home():
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return authError
        else:

            CommonVar.accountData = jsonIO.load_data("data/accountData.json")
            data = [item for item in CommonVar.accountData if item["AccountID"] == session['username'] ][0]

            return render_template('home.html',accountData = data, role = session['username'][0] )
            
    @app.route("/initialize", methods=['GET', 'POST'])
    def initialize():
        if request.method == 'POST':
            password = request.form['password']

            with open("data/auth.json", 'w') as file:
                hashed_password = generate_password_hash(password)
                data = []
                
                data.append({
                    'username': '30000000',
                    'password': str(hashed_password)
                })
                print(f"The password has been set and the administrator username is (\"3\" + 7個0)'30000000'")

                CommonVar.initialize = False
                json.dump(data, file)
            return redirectPage('/login', "The password has been set. Please Login now")
        else:
            return render_template('initialize.html')

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if CommonVar.initialize == True:
            return redirect(url_for('initialize'))

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            auth = jsonIO.load_data("data/auth.json")
            users = []
            for dat in auth:
                users.append(dat['username'])
            # 檢查使用者名稱是否存在
            if username not in users:
                return redirectPage("/login", "This username does not exist, please contact IT staff for assistance。")

            # 檢查密碼是否匹配
            for dat in auth:
                if dat['username'] == username:
                    hash = dat['password']

            if not check_password_hash(hash, password):
                return redirectPage("/login", "Wrong password, please re-enter. \nIf you forget your password, please contact IT staff for assistance.")

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