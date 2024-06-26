import logging as logger
from app import *
import pymongo
from api.wrap.auth import AppResource

def get_db_reference(type):
    if type == 'poem':
        return mongo.db.poems
    elif type == 'blog':
        return mongo.db.blogs
    elif type == 'musing':
        return mongo.db.musings
    elif type == 'prompt':
        return mongo.db.prompts


class Post(AppResource):

    def __init__(self):
        self.users = mongo.db.users
        self.followersRef = mongo.db.followers
        self.followingRef = mongo.db.following
        pass

    def post(self, type):
        userID = request.args['userID']
        self.users.update_one({'_id':userID},{'$inc':{'posts':1}})
        postDict = request.get_json(force=True)
        rawFollowers=self.followersRef.find_one({'_id':userID},{'followersList.userID':1})
        doc_id = get_db_reference(type).insert_one(postDict).inserted_id
        postDict['_id']=doc_id
        self.followingRef.update({'_id': {'$in': rawFollowers['followersList']}},{'$addToSet':{'feed':postDict}},upsert=True,multi=True)
        return {}, 200

    def get(self, type):
        # if last id is null return first few items upto the limit
        # if last id is not null return all items from the next item of last id upto the limit
        output = []
        firstPosts = None
        limit = int(request.args['limit'])
        filter = request.args['filter']
        if filter == 'newest':
            try:
                lastDocumentID = request.args['last_id']
            except:
                firstPosts = get_db_reference(type).find(sort=[('_id', pymongo.DESCENDING)]).limit(limit)
                for i in firstPosts:
                    i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
                    output.append(i)
                return output, 200
            posts = get_db_reference(type).find({'_id': {'$lt': ObjectId((lastDocumentID))}}).sort('_id',
                                                                                                   pymongo.DESCENDING).limit(
                limit)
            for i in posts:
                i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
                output.append(i)
            return output, 200
        elif filter == 'top':
            try:
                lastDocumentID = request.args['last_id']
            except:
                dt = datetime.utcnow() - timedelta(days=7,hours=12)
                objID=ObjectId.from_datetime(dt)
                app.logger.info(objID)
                firstPosts = get_db_reference(type).find({'_id':{'$lt':ObjectId(objID)}},sort=[('likes', pymongo.DESCENDING)]).limit(limit)
                for i in firstPosts:
                    i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
                    output.append(i)
                return output, 200
            posts = get_db_reference(type).find({'_id': {'$gt': ObjectId((lastDocumentID))}}).sort('likes',
                                                                                                   pymongo.DESCENDING).limit(
                limit)
            for i in posts:
                i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
                output.append(i)
            return output, 200

    def put(self, type):
        pass

    def delete(self, type):
        pass
