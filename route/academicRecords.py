








from flask import render_template, session
from utilities import jsonIO, utilities


def load(app, accountData):
    @app.route("/academicRecords/<AccountID>/")
    @app.route("/academicRecords/<AccountID>")
    def academicRecords_adminVer(AccountID):
        authError = utilities.authVerify(app, 3)
        if authError is not None:
            return authError
        else:
            academicRecordsDatas = jsonIO.load_data("data/academicRecordsData.json")
            for academicRecordsData in academicRecordsDatas:
                if academicRecordsData['AccountID'] == AccountID:
                    data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
                    return render_template('academicRecords.html',accountData = data,  academicRecordsData = academicRecordsData)
            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
            return render_template('academicRecords.html',accountData = data,academicRecordsData = {})

    @app.route("/academicRecords")
    def academicRecords():
        authError = utilities.authVerify(app, 1)
        if authError is not None:
            return authError
        else:
            global accountData
            accountData = jsonIO.load_data("data/accountData.json")
            academicRecordsDatas = jsonIO.load_data("data/academicRecordsData.json")
            for academicRecordsData in academicRecordsDatas:
                if academicRecordsData['AccountID'] == session['username']:
                    data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
                    return render_template('academicRecords.html',accountData = data,  academicRecordsData = academicRecordsData)
            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
            return render_template('academicRecords.html',accountData = data,academicRecordsData = {})
    
    
    @app.route("/academicRecords/<AccountID>")
    def academicRecords_tecVer(AccountID):
        authError = utilities.authVerify(app, 2)
        if authError is not None:
            return authError
        else:
            global accountData
            accountData = jsonIO.load_data("data/accountData.json")
            academicRecordsDatas = jsonIO.load_data("data/academicRecordsData.json")
            for academicRecordsData in academicRecordsDatas:
                if academicRecordsData['AccountID'] == AccountID:
                    data = [item for item in accountData if item["AccountID"] == AccountID[0]]
                    return render_template('academicRecords.html',accountData = data,  academicRecordsData = academicRecordsData)
            data = [item for item in accountData if item["AccountID"] == session['username'] ][0]
            return render_template('academicRecords.html',accountData = data,academicRecordsData = {})
