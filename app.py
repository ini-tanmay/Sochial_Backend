from flask import Flask, jsonify,request
from flask_pymongo import PyMongo
import json
import logging
logging.basicConfig(level=logging.DEBUG)
from bson.objectid import ObjectId
class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class MyConfig(object):
    RESTFUL_JSON = {'cls': JsonEncoder}


# get poems with pagination
# add poem
# get poems by userID
# get poem by poemID

app = Flask(__name__)
DB_URI = "mongodb+srv://sochial:voltairemensutrabhai@cluster0.7lovb.mongodb.net/gigat?retryWrites=true&w=majority"
app.config['MONGO_DBNAME'] = 'gigat'
app.config['MONGO_URI'] = DB_URI
app.json_encoder = JsonEncoder
app.config.from_object(MyConfig)
# MyConfig. (app)
mongo = PyMongo(app)
from api import *

#
# {
#     "_id": "tanmay".
#     "username": "tanmay",
#
#     "name": "name"
# }

# userID = request.args['username']
# bio = request.args['bio']
# fcm
# userID = request.args['name']
# websiteLink = request.args['websiteLink']

@app.route('/api/v1.0/users/username/<string:username>')
def is_user_taken(username):
    users = mongo.db.users
    user = users.find_one({'usern': username})
    if user is None:
        return jsonify(False)
    else:
        return jsonify(True)


@app.route('/')
def hello():
    return 'Hey'


if __name__ == '__main__':
    app.run(threaded=True)

