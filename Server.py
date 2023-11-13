from datetime import datetime, timedelta
import os
from flask import Flask, jsonify, render_template_string, request, render_template, redirect, send_file, url_for , session
import jwt
from werkzeug.security import check_password_hash
import utilities.jsonIO as jsonIO
from utilities.initialize import initialize
from werkzeug.utils import secure_filename
from tools.register import excel_to_json, singelReg
from urllib.parse import unquote
from utilities.utilities import *
import uuid
import json

from route import personalInfo, academicRecords,adminTool,coursePage, redirectPage, authRoute


app = Flask(__name__)

# 系統亂數種子
app.secret_key = 'your_secret_keya'




if __name__ == "__main__":
    # 檢查系統是否已經初始化
    initialize()
    accountData = jsonIO.load_data("data/accountData.json")

    personalInfo.load(app,accountData)
    academicRecords.load(app,accountData)
    adminTool.load(app,accountData)
    coursePage.load(app,accountData)
    authRoute.load(app,accountData)

    app.run(host= '0.0.0.0' ,port=5000,debug=True)