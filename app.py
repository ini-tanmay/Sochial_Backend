from flask import Flask, jsonify, request, current_app
from flask_pymongo import PyMongo
import json
import logging
from notificationservice import NotificationService
from datetime import datetime
from math import sqrt
from collections import Counter
import pymongo

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
# restServerInstance.add_resource(User, "/api/v1.0/users/id/<string:userID>/followers")
# restServerInstance.add_resource(User, "/api/v1.0/users/id/<string:userID>/followers")
# restServerInstance.add_resource(User, "/api/v1.0/users/id/<string:userID>/following/")
# restServerInstance.add_resource(User, "/api/v1.0/users/id/<string:userID>/timeline")

@app.route('/api/v1.0/users/id/<string:userID>/followers/<int:last_no>', endpoint='fiuu')
def get_followers_list(userID, last_no):
    output = []
    followers = mongo.db.followers
    users = followers.find({'_id': userID}, {'followersList': {'$slice': [last_no * 30, (last_no + 1) * 30]}})
    for i in users:
        output.append(i['followersList'])
    return jsonify(output)


@app.route('/api/v1.0/users/id/<string:userID>/posts/id/<string:postID>/inc/<string:type>')
def incrementLikes(userID, postID, type):
    poems = mongo.db.poems
    musings = mongo.db.musings
    prompts = mongo.db.prompts
    if type == 'poems':
        poems.update({'_id': ObjectId(postID)}, {'$inc': {'likes': 1}, '$push': {'likedBy': userID}})
    elif type == 'musings':
        musings.update({'_id': ObjectId(postID)}, {'$inc': {'likes': 1}, '$push': {'likedBy': userID}})
    else:
        prompts.update({'_id': ObjectId(postID)}, {'$inc': {'likes': 1}, '$push': {'likedBy': userID}})
    return jsonify([]);


@app.route('/api/v1.0/users/id/<string:userID>/posts/id/<string:postID>/inc')
def incrementViews(userID, postID):
    poems = mongo.db.poems
    if type == 'poem':
        poems.update({'_id': ObjectId(postID)}, {'$inc': {'views': 1}, '$push': {'viewedBy': userID}})
    return jsonify([]);


@app.route('/api/v1.0/users/id/<string:userID>/posts/id/<string:postID>/dec/<string:type>')
def decrementLikes(userID, postID, type):
    poems = mongo.db.poems
    musings = mongo.db.musings
    prompts = mongo.db.prompts
    if type == 'poem':
        poems.update({'_id': ObjectId(postID)}, {'$inc': {'likes': -1}, '$pull': {'likedBy': userID}})
    elif type == 'musing':
        musings.update({'_id': ObjectId(postID)}, {'$inc': {'likes': -1}, '$pull': {'likedBy': userID}})
    else:
        prompts.update({'_id': ObjectId(postID)}, {'$inc': {'likes': -1}, '$pull': {'likedBy': userID}})
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

#@app.route('loaderio-5766de92b38d3cc2e912db60eeb642db.txt')
#def loading():
 #   return current_app.send_static_file('loader_file.txt')

# @app.route('/api/v1.0/poems/id/update')
# def update():
#     poems=mongo.db.poems
#     musings=mongo.db.musings
#     prompts=mongo.db.prompts
#     poems.update({},{'$set':{'likes':1,'comments':0,'views':1,'likedBy':['Duregm8wDUUoIyG7DQzLKw136hf2'],'viewedBy':['Duregm8wDUUoIyG7DQzLKw136hf2']}},multi=True)
#     prompts.update({},{'$set':{'likes':1,'comments':0,'views':1,'likedBy':['Duregm8wDUUoIyG7DQzLKw136hf2']}},multi=True)
#     musings.update({},{'$set':{'likes':1,'comments':0,'views':1,'likedBy':['Duregm8wDUUoIyG7DQzLKw136hf2']}},multi=True)

@app.route('/api/v1.0/users/id/<string:userID>/follow/posts')
def get_posts_from_who_i_follow(userID):
    output = []
    poemsList = []
    musingsList = []
    promptsList = []
    followers = mongo.db.followers
    poems = mongo.db.poems
    musings = mongo.db.musings
    prompts = mongo.db.prompts
    users = followers.find({}, {
        'followersList': {'$elemMatch': {'_id': ObjectId(userID)}}})
    # ObjectId.fromDate(datetime.utcnow())
    #  ISODate("2018-01-24T06:09:42Z")

    for i in users:
        poemsFound = poems.find({"$and": [{"userID": {'$e': str(i['_id'])}},
                                          {"_id": {'$gte': ObjectId.fromDate(datetime.utcnow())}}]}).sort('_id',
                                                                                                          pymongo.ASCENDING)
        for p in poemsFound:
            poemsList.append(p)
        # musings
        musingsFound = musings.find({"$and": [{"userID": {'$e': str(i['_id'])}},
                                              {"_id": {'$gte': ObjectId.fromDate(datetime.utcnow())}}]}).sort('_id',
                                                                                                              pymongo.ASCENDING)
        for m in musingsFound:
            musingsList.append(m)
        # prompts
        promptsFound = prompts.find({"$and": [{"userID": {'$e': str(i['_id'])}},
                                              {"_id": {'$gte': ObjectId.fromDate(datetime.utcnow())}}]}).sort('_id',
                                                                                                              pymongo.ASCENDING)
        for pr in promptsFound:
            promptsList.append(pr)
    output.extend(poemsList)
    output.extend(promptsList)
    output.extend(musingsList)
    return jsonify(output)


@app.route('/api/v1.0/posts/best')
def get_best_posts():
    poemsRef = mongo.db.poems
    musingsRef = mongo.db.musings
    promptsRef = mongo.db.prompts
    usersRef=mongo.db.users
    year = datetime.utcnow().date().year
    month = datetime.utcnow().date().month
    day = datetime.utcnow().date().day-8
    date_time_str = str(year) + '-' + str(month) + '-' + str(day)
    d = datetime.strptime(date_time_str, '%Y-%m-%d')
    app.logger.info(d)
    dt = d
    result = list(poemsRef.find({'_id': {'$gte': ObjectId.from_datetime(dt)}}).sort('_id', pymongo.ASCENDING))
    result.extend(
        list(musingsRef.find({'_id': {'$gte': ObjectId.from_datetime(dt)}}).sort('_id', pymongo.ASCENDING)))
    result.extend(
        list(promptsRef.find({'_id': {'$gte': ObjectId.from_datetime(dt)}}).sort('_id', pymongo.ASCENDING)))
    for i in result:
        if i['views'] is None:
            i['views'] = 1
        i['score'] = get_score(i['likes'], i['views'])
    posts = sorted(result, key=lambda i: i['score'])
    for i in posts[:150]:
        user=usersRef.find_one({'_id':i['userID']},{'fcm':1})
        try:
            title=i[title]
        except:
            title=None
        NotificationService().send_featured_message(user['fcm'],title,i['text'])
    return jsonify(posts[:150])


def get_score(likes, views):
    downs = views - likes
    n = likes - 1 + downs
    if n <= 0:
        return 0
    z = 1.44  # 1.44 = 85%, 1.96 = 95%
    phat = float(likes) / n
    return ((phat + z * z / (2 * n) - z * sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n))


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
                         {'$push': {'followersList': myUserDict}, '$set': {'name': name, 'usern': username}},
                         upsert=True)
    return jsonify(True)


@app.route('/api/v1.0/users/id/<string:myUserID>/unfollow/<string:otherUserID>')
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
    app.logger.debug("Starting Flask Server")
    app.run(threaded=True)
