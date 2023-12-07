from datetime import datetime
from flask import Flask
import utilities.jsonIO as jsonIO
from utilities.initialize import initialize
from utilities.utilities import *
from utilities import CommonVar

from route import personalInfo, academicRecords,adminTool,coursePage, redirectPage, authRoute


app = Flask(__name__)

# System Seed
app.secret_key = str(datetime.now())




if __name__ == "__main__":

    initialize()
    
    personalInfo.load(app)
    academicRecords.load(app)
    adminTool.load(app)
    coursePage.load(app)
    authRoute.load(app)

    app.run(host= '0.0.0.0' ,port=5000)