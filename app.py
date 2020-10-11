from flask import Flask, jsonify, request, current_app, redirect
from flask_pymongo import PyMongo
import json
import logging
from notificationservice import NotificationService
from datetime import datetime, timedelta
from math import sqrt
from collections import Counter
import pymongo
from scout_apm.flask import ScoutApm
from bson.objectid import ObjectId
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from functools import wraps

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        headers = request.headers
        try:
            decoded_token = auth.verify_id_token(headers['Authorization'])
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            app.logger.info(e)
            flask_restful.abort(401)

    return wrapper



class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class MyConfig(object):
    RESTFUL_JSON = {'cls': JsonEncoder}


app = Flask(__name__)
DB_URI = "mongodb+srv://sochial:7a7ff0b9mensutra@cluster0.7lovb.mongodb.net/gigat?retryWrites=true&w=majority"
app.config['MONGO_DBNAME'] = 'gigat'
app.config['MONGO_URI'] = DB_URI
app.json_encoder = JsonEncoder
app.config.from_object(MyConfig)
# jwt-JWT(app=app)
mongo = PyMongo(app)
ScoutApm(app)
app.config["SCOUT_NAME"] = "Sochial"

from api import *


@app.route('/api/v1.0/user/id/<string:userID>/followers/<int:last_no>', endpoint='get_followers')
@authenticate
def get_followers_list(userID, last_no):
    output = []
    followers = mongo.db.followers
    users = followers.find({'_id': userID}, {'followersList': {'$slice': [last_no * 30, (last_no + 1) * 30]}})
    for i in users:
        output.append(i['followersList'])
    return jsonify(output)


@app.route('/api/v1.0/user/id/<string:userID>/following/<int:last_no>', endpoint='get_following')
@authenticate
def get_following_list(userID, last_no):
    output = []
    following = mongo.db.following
    users = following.find({'_id': userID}, {'followingList': {'$slice': [last_no * 30, (last_no + 1) * 30]}})
    for i in users:
        output.append(i['followingList'])
    return jsonify(output)


@app.route('/api/v1.0/user/id/<string:myUserID>/follows/<string:otherUserID>/check', endpoint='check_if_i_f_o')
@authenticate
def does_user_follow_otherUser(myUserID, otherUserID):
    following = mongo.db.following
    user = followers.find({'_id': myUserID}, {'followingList': {'$elemMatch': {'userID': otherUserID}}})
    if 'followingList' in list(user)[0]:
        return jsonify(True)
    return jsonify(False)


@app.route('/api/v1.0/user/id/<string:userID>/l/<string:type>/id/<string:postID>', methods=['PUT'])
@authenticate
def incrementLikes(userID, postID, type):
    get_db_reference(type).update({'_id': ObjectId(postID)}, {'$inc': {'likes': 1}, '$addToSet': {'likedBy': userID}})
    return jsonify([])


@app.route('/api/v1.0/user/id/<string:userID>/dl/<string:type>/id/<string:postID>', methods=['PUT'])
@authenticate
def decrementLikes(userID, postID, type):
    if (type == blog):
        get_db_reference(type).update({'_id': ObjectId(postID)},
                                      {'$inc': {'dislikes': 1}, '$push': {'likedBy': userID}})
        return jsonify(True)
    get_db_reference(type).update({'_id': ObjectId(postID)}, {'$inc': {'likes': -1}, '$pull': {'likedBy': userID}})
    return jsonify([])


@app.route('/loaderio-5766de92b38d3cc2e912db60eeb642db.txt')
def testing_func():
    return current_app.send_static_file('loader_file.txt')

@app.route('/api/v1.0/userr/id/<string:userID>/following/posts/<int:last_no>')
@authenticate
def get_posts_from_who_i_follow(userID,last_no):
    output = []
    following=mongo.db.following
    output = list(following.find({'_id': userID}, {'feed': {'$slice': [last_no * 10, (last_no + 1) * 10]}}))
    return jsonify(output)



# @app.route('/api/v1.0/following/posts', methods=['POST'])
# @authenticate
# def get_posts_from_who_i_follow():
#     output = []
#     poemsRef = mongo.db.poems
#     musingsRef = mongo.db.musings
#     promptsRef = mongo.db.prompts
#     DD = timedelta(days=40)
#     users = request.get_json(force=True)['users']
#     dateTime = datetime.utcnow() - DD
#     objID = ObjectId.from_datetime(dateTime)
#     app.logger.info(users)
#     app.logger.info(type(users))
#     for user in users:
#         output.extend(poemsRef.find({'$and': [{'userID': user}, {'_id': {'$gte': objID}}]}).sort('_id',
#                                                                                                  pymongo.ASCENDING).limit(
#             2))
#         output.extend(musingsRef.find({'$and': [{'userID': user}, {'_id': {'$gte': objID}}]}).sort('_id',
#                                                                                                    pymongo.ASCENDING).limit(
#             2))
#         output.extend(promptsRef.find({'$and': [{'userID': user}, {'_id': {'$gte': objID}}]}).sort('_id',
#                                                                                                    pymongo.ASCENDING).limit(
#             2))
#     # if len(output)<=5:
#     return jsonify(output)


@app.route('/api/v1.0/posts/best', endpoint='get_best_posts')
@authenticate
def get_best_posts():
    poemsRef = mongo.db.poems
    musingsRef = mongo.db.musings
    promptsRef = mongo.db.prompts
    usersRef = mongo.db.users
    dt = datetime.now() - timedelta(days=30)
    result = list(
        poemsRef.find({'_id': {'$gte': ObjectId.from_datetime(dt)}}).sort('likes', pymongo.DESCENDING).limit(100))
    result.extend(
        list(
            musingsRef.find({'_id': {'$gte': ObjectId.from_datetime(dt)}}).sort('likes', pymongo.DESCENDING).limit(25)))
    result.extend(
        list(
            promptsRef.find({'_id': {'$gte': ObjectId.from_datetime(dt)}}).sort('likes', pymongo.DESCENDING).limit(25)))
    posts = sorted(result, key=lambda i: i['likes'])
    for i in posts[:150]:
        i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
        user = usersRef.find_one({'_id': i['userID']}, {'fcm': 1})
        # try:
        #     title = i[title]
        # except:
        #     title = None
        # NotificationService().send_featured_message(user['fcm'], title, i['text'])
    return jsonify(posts[:150])


@app.route('/api/v1.0/posts/blogs/best', endpoint='get_best_blogs')
@authenticate
def get_best_blogs():
    blogsRef = mongo.db.blogs
    usersRef = mongo.db.users
    dt = datetime.utcnow() - timedelta(days=30)
    try:
        lastID = request.args['last_id']
        result = list(
            blogsRef.find({'_id': {'$gt': ObjectId(lastID)}}).sort('_id', pymongo.ASCENDING).limit(4))
    except:
        result = list(
            blogsRef.find({'_id': {'$gt': ObjectId.from_datetime(dt)}}).sort('_id', pymongo.ASCENDING).limit(4))

    app.logger.info(list(result))
    for i in result:
        i['score'] = get_score(i['likes'] + 1, i['dislikes'] + 1)
    posts = sorted(result, key=lambda i: i['score'])
    for i in posts[:150]:
        i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
    #     user = usersRef.find_one({'_id': i['userID']}, {'fcm': 1})
    # try:
    #     title = i[title]
    # except:
    #     title = None
    # NotificationService().send_featured_message(user['fcm'], title)
    return jsonify(posts[:150])


def get_score(likes, views):
    n = views - likes
    if n <= 0:
        return 0
    z = 1.44  # 1.44 = 85%, 1.96 = 95%
    phat = float(likes) / n
    return ((phat + z * z / (2 * n) - z * sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n))


def get_db_reference(type):
    if type == 'poem':
        return mongo.db.poems
    elif type == 'blog':
        return mongo.db.blogs
    elif type == 'musing':
        return mongo.db.musings
    elif type == 'prompt':
        return mongo.db.prompts


@app.route('/api/v1.0/user/id/<string:userID>/b/user/id/<string:otherUserID>',
           methods=['POST'])
@authenticate
def myuser_blocks_otheruser(userID, otherUserID):
    users = mongo.db.users
    users.update_one({'_id': (userID)}, {'$addToSet': {'blocked': (otherUserID)}}, upsert=True)
    return jsonify({})


@app.route('/api/v1.0/<string:userID>/r/<string:type>/id/<string:postID>',
           methods=['POST'])
@authenticate
def report_post(userID, type, postID):
    reported = mongo.db.reported
    reported.update_one({'_id': ObjectId(postID)}, {'$addToSet': userID}, {'$set': {'type': type}},upsert=True)
    return jsonify({})


@app.route('/api/v1.0/follow',
           methods=['POST'])
@authenticate
def myuser_follows_otheruser():
    followers = mongo.db.followers
    following = mongo.db.following
    otherFcmToken=request.args['server_log']
    myUserDict = dict(request.get_json(force=True))['my']
    otherUserDict=dict(request.get_json(force=True))['other']
    users.update_one({'_id': myUserDict['userID']}, {'$inc': {'following': 1}})
    users.update_one({'_id': otherUserDict['userID']}, {'$inc': {'followers': 1}})
    NotificationService().send_message(otherFcmToken, myUserDict['name'], myUserDict['usern'])
    followers.update_one({'_id': (otherUserID)},
                         {'$addToSet': {'followersList': myUserDict}},
                         upsert=True)
    following.update_one({'_id': (myUserDict['userID'])},
                         {'$addToSet': {'followingList': otherUserDict}},
                         upsert=True)
    return jsonify(True)


@app.route('/api/v1.0/user/id/<string:myUserID>/unfollowed/<string:otherUserID>', methods=['DELETE'])
@authenticate
def myuser_unfollows_otheruser(myUserID, otherUserID):
    followers = mongo.db.followers
    following = mongo.db.following
    users.update_one({'_id': (myUserID)}, {'$inc': {'following': -1}})
    users.update_one({'_id': (otherUserID)},
                     {'$inc': {'followers': -1}})
    followers.update_one({'_id': otherUserID}, {'$pull': {'followersList': myUserID}})
    following.update_one({'_id': myUserID}, {'$pull': {'followingList': otherUserID}})
    return jsonify(True)


@app.route('/api/v1.0/users/username/<string:username>')
@authenticate
def is_username_taken(username):
    users = mongo.db.users
    user = users.find_one({'usern': username})
    if user is None:
        return jsonify(False)
    else:
        return jsonify(True)


@app.route('/')
def hello():
    return redirect("https://www.sochial.media", code=302)

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate("static/sochial-readme.json")
        firebase_admin.initialize_app(cred)
except Exception as e:
    print(e)
    app.logger.error(e)


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == '__main__':
    app.logger.debug("Starting Flask Server")
    app.run(threaded=True)
