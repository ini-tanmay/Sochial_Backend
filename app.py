from flask import Flask, jsonify, request, current_app
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

@app.route('/api/v1.0/users/id/<string:userID>/followers/<int:last_no>', endpoint='get_followers')
def get_followers_list(userID, last_no):
    output = []
    followers = mongo.db.followers
    users = followers.find({'_id': userID}, {'followersList': {'$slice': [last_no * 30, (last_no + 1) * 30]}})
    for i in users:
        output.append(i['followersList'])
    return jsonify(output)


@app.route('/api/v1.0/users/id/<string:myUserID>/follows/<string:otherUserID>/check', endpoint='check_if_i_f_o')
def does_user_follow_otherUser(myUserID, otherUserID):
    followers = mongo.db.followers
    user = followers.find({'_id': otherUserID}, {'followersList': {'$elemMatch': {'_id': myUserID}}})
    for i in user:
        if 'followersList' in i:
            return jsonify(True)
    return jsonify(False)


@app.route('/api/v1.0/users/id/<string:userID>/posts/id/<string:postID>/l/inc/<string:type>', methods=['PUT'])
def incrementLikes(userID, postID, type):
    get_db_reference(type).update({'_id': ObjectId(postID)}, {'$inc': {'likes': 1}, '$addToSet': {'likedBy': userID}})
    return jsonify([]);


@app.route('/api/v1.0/users/id/<string:userID>/posts/id/<string:postID>/dec/<string:type>', methods=['PUT'])
def decrementLikes(userID, postID, type):
    get_db_reference(type).update({'_id': ObjectId(postID)}, {'$inc': {'likes': -1}, '$pull': {'likedBy': userID}})
    return jsonify([]);


@app.route('/api/v1.0/users/id/<string:userID>/following')
def get_following_list(userID):
    output = []
    followers = mongo.db.followers
    users = followers.find({}, {
        'followersList': {'$elemMatch': {'_id': userID}}
        , '_id': 1, 'name': 1, 'usern': 1})
    for i in users:
        output.append(i)
    return jsonify(output)


@app.route('/loaderio-5766de92b38d3cc2e912db60eeb642db.txt')
def testing_func():
    return current_app.send_static_file('loader_file.txt')


@app.route('/api/v1.0/users/id/<string:userID>/following/posts/<int:page>')
def get_posts_from_who_i_follow(userID, page):
    output = []
    poemsRef = mongo.db.poems
    musingsRef = mongo.db.musings
    promptsRef = mongo.db.prompts
    usersRef = mongo.db.users
    followers = mongo.db.followers
    users = list(followers.find_one({}, {
        'followersList': {'$elemMatch': {'_id': userID}}
        , '_id': 1}))
    DD = timedelta(days=2)
    dateTime = datetime.utcnow() - DD
    objID = ObjectId.from_datetime(dateTime)
    first = max(len(users) - 15, page * 15)
    second = max(len(users) - first, (page + 1) * 15)
    for user in users[first:second]:
        result = []
        result.extend(poemsRef.find({'$and': [{'userID': user['_id']}, {'_id': {'$gte': objID}}]}).sort('_id',
                                                                                                        pymongo.ASCENDING).limit(
            3))
        result.extend(musingsRef.find({'$and': [{'userID': user['_id']}, {'_id': {'$gte': objID}}]}).sort('_id',
                                                                                                          pymongo.ASCENDING).limit(
            3))
        result.extend(promptsRef.find({'$and': [{'userID': user['_id']}, {'_id': {'$gte': objID}}]}).sort('_id',
                                                                                                          pymongo.ASCENDING).limit(
            3))
        output.extend(result)
        result.clear()
    return jsonify(output)


@app.route('/api/v1.0/posts/best', endpoint='get_best_posts')
def get_best_posts():
    poemsRef = mongo.db.poems
    musingsRef = mongo.db.musings
    promptsRef = mongo.db.prompts
    usersRef = mongo.db.users
    year = datetime.utcnow().date().year
    month = datetime.utcnow().date().month
    day = datetime.utcnow().date().day - 1
    date_time_str = str(year) + '-' + str(month) + '-' + str(day)
    dt = datetime.strptime(date_time_str, '%Y-%m-%d')
    result = list(poemsRef.find({'_id': {'$gte': ObjectId.from_datetime(dt)}}).sort('_id', pymongo.ASCENDING))
    result.extend(
        list(musingsRef.find({'_id': {'$gte': ObjectId.from_datetime(dt)}}).sort('_id', pymongo.ASCENDING)))
    result.extend(
        list(promptsRef.find({'_id': {'$gte': ObjectId.from_datetime(dt)}}).sort('_id', pymongo.ASCENDING)))
    for i in result:
        i['score'] = get_score(i['likes'], 0)
    posts = sorted(result, key=lambda i: i['score'])
    for i in posts[:150]:
        i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
        user = usersRef.find_one({'_id': i['userID']}, {'fcm': 1})
        try:
            title = i[title]
        except:
            title = None
        NotificationService().send_featured_message(user['fcm'], title, i['text'])
    return jsonify(posts[:150])


@app.route('/api/v1.0/posts/blogs/best', endpoint='get_best_blogs')
def get_best_blogs():
    blogsRef = mongo.db.blogs
    usersRef = mongo.db.users
    year = datetime.utcnow().date().year
    month = datetime.utcnow().date().month
    day = datetime.utcnow().date().day - 1
    date_time_str = str(year) + '-' + str(month) + '-' + str(day)
    dt = datetime.strptime(date_time_str, '%Y-%m-%d')
    result = list(
        blogsRef.find({'_id': {'$gte': ObjectId.from_datetime(dt)}}).sort('_id', pymongo.ASCENDING).limit(150))
    app.logger.info(list(result))
    for i in result:
        i['score'] = get_score(i['likes'], i['dislikes'])
    posts = sorted(result, key=lambda i: i['score'])
    for i in posts[:150]:
        user = usersRef.find_one({'_id': i['userID']}, {'fcm': 1})
        try:
            title = i[title]
        except:
            title = None
        NotificationService().send_featured_message(user['fcm'], title)
    return jsonify(posts[:150])


def get_score(likes, views):
    downs = views - likes
    n = likes - 1 + downs
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
def myuser_blocks_otheruser(userID, otherUserID):
    users = mongo.db.users
    users.update_one({'_id': (userID)}, {'$addToSet': {'blocked': (otherUserID)}}, upsert=True)
    return jsonify({})


@app.route('/api/v1.0/users/id/<string:otherUserID>/name/<string:name>/username/<string:username>/follow',
           methods=['POST'])
def myuser_follows_otheruser(otherUserID, name, username):
    followers = mongo.db.followers
    users = mongo.db.users
    myUserDict = dict(request.get_json(force=True))
    users.update_one({'_id': myUserDict['_id']}, {'$inc': {'following': 1}})
    users.update_one({'_id': (otherUserID)}, {'$inc': {'followers': 1}})
    NotificationService().send_message(myUserDict['otherFcm'], myUserDict['name'], myUserDict['usern'])
    myUserDict.pop('otherFcm')
    followers.update_one({'_id': (otherUserID)},
                         {'$addToSet': {'followersList': myUserDict}, '$set': {'name': name, 'usern': username}},
                         upsert=True)
    return jsonify(True)


@app.route('/api/v1.0/users/id/<string:myUserID>/unfollow/<string:otherUserID>', methods=['PUT'])
def myuser_unfollows_otheruser(myUserID, otherUserID):
    followers = mongo.db.followers
    users = mongo.db.users
    users.update_one({'_id': (myUserID)}, {'$inc': {'following': -1}})
    users.update_one({'_id': (otherUserID)}, {'$inc': {'followers': -1}})
    followers.update(
        {"_id": (otherUserID)},
        {
            "$pull": {
                "followersList": {"_id": (myUserID)}
            }
        })
    return jsonify(True)


@app.route('/api/v1.0/users/username/<string:username>')
def is_usaername_taken(username):
    users = mongo.db.users
    user = users.find_one({'usern': username})
    if user is None:
        return jsonify(False)
    else:
        return jsonify(True)


@app.route('/')
def hello():
    return 'Hey'

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


if __name__ == '__main__':
    app.logger.debug("Starting Flask Server")
    try:
        if not firebase_admin._apps:
             cred = credentials.Certificate("static/sochial-readme.json")
             firebase_admin.initialize_app(cred)
    except Exception as e:
        print(e)
        app.logger.error(e)

    app.run(threaded=True)
