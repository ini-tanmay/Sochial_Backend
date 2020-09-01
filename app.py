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


@app.route('/users/<userID>')
def get_user_by_userID(userID):
    users = mongo.db.users
    user = users.find_one({'_id':(userID)})
    #gets json and converts it to dict
    app.logger.info(user)
    app.logger.info(type(user))
    if user is not None:
        output = json.dumps(user)
    else:
        output = {'result':'no results lol'}
    return output


@app.route('/users', methods=['POST'])
def add_user():
    users=mongo.db.users
    req_data = request.get_json(force=True)
    #gets json and converts it to dict
    app.logger.info('--------------')
    app.logger.info(req_data)
    app.logger.info(type(req_data))
    app.logger.info('--------------')
    users.insert_one(req_data)
    #check if correct
    new_framework = users.find_one({'_id':req_data['_id']})
    return jsonify({'result': new_framework})

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

@app.route('/users')
def get_all_users():
    users = mongo.db.users
    output = []
    for q in users.find():
        app.logger.info(type(q))
        app.logger.info(q)
        output.append(q)
    return jsonify(output)


@app.route('/')
def hello():
    return 'Hey'


if __name__ == '__main__':
    app.logger.debug("Starting Flask Server")
    from api import *
    app.run(host='192.168.1.69', port=8000, debug=False,use_reloader=True)
