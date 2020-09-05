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

@app.route('/api/v1.0/users/id/<string:userID>/followers/<int:last_no>', endpoint='get_followers_list')
def get_followers_list(userID, last_no):
    output = []
    followers = mongo.db.followers
    users = followers.find({'_id': ObjectId(userID)}, {'followersList': {'$slice': [last_no * 30, (last_no + 1) * 30]}})
    for i in users:
        output.append(i['followersList'])
    return jsonify(output[0])


@app.route('/api/v1.0/users/id/<string:userID>/following',endpoint='get_following_list')
def get_following_list(userID):
    output = []
    followers = mongo.db.followers
    users = followers.find({}, {
        'followersList': {'$elemMatch': {'_id': ObjectId(userID)}}
        , '_id': 1, 'name': 1, 'usern': 1})
    for i in users:
        output.append(i)
    return jsonify(output)


@app.route('/api/v1.0/users/id/<string:otherUserID>/name/<string:name>/username/<string:username>/follow',endpoint='follow_other_user')
           methods=['POST'])
def myuser_follows_otheruser(otherUserID, name, username):
    followers = mongo.db.followers
    myUserDict = request.get_json(force=True)
    myUserDict['_id'] = ObjectId(myUserDict['_id'])
    followers.update_one({'_id': ObjectId(otherUserID)},
                         {'$push': {'followersList': myUserDict}, '$set': {'name': name, 'usern': username}},
                         upsert=True)
    return jsonify(True)


@app.route('/api/v1.0/users/id/<string:myUserID>/unfollow/<string:otherUserID>',endpoint='unfollow_other_user')
def myuser_unfollows_otheruser(myUserID, otherUserID):
    followers = mongo.db.followers
    followers.update(
        {"_id": ObjectId(otherUserID)},
        {
            "$pull": {
                "followersList": {"_id": ObjectId(myUserID)}
            }
        })
    return jsonify(True)


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

