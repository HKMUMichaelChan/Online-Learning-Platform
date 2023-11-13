
from datetime import datetime, timedelta
import jwt
from werkzeug.security import check_password_hash
from flask import redirect, render_template, request, session, url_for
from route.redirectPage import redirectPage
from utilities import jsonIO, utilities



def load(app, accountData):
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

            global accountData
            accountData = jsonIO.load_data("data/accountData.json")
            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]

            return render_template('home.html',accountData = data, role = session['username'][0] )
            

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            auth = jsonIO.load_data("data/auth.json")
            users = []
            for dat in auth:
                users.append(dat['username'])
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