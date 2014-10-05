from flask import Flask
from flask.ext.cors import CORS
app = Flask(__name__)
CORS(app, resources=r'/*', headers='Content-Type')

#----------------------------------------
# database
#----------------------------------------

from mongoengine import connect
from flask.ext.mongoengine import MongoEngine

DB_NAME = 'passapp'
DB_USERNAME = 'pavol'
DB_PASSWORD = 'pavol'
DB_HOST_ADDRESS = 'ds063859.mongolab.com:63859/passapp'

app.config["MONGODB_DB"] = DB_NAME
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
db = MongoEngine(app)


#----------------------------------------
# api
#----------------------------------------

import restapi


api = restapi.Api(app)    

if __name__ == '__main__':
    app.run(debug=True)
