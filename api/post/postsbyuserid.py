from api.wrap.auth import AppResource
import logging as logger
from app import *
import pymongo
from datetime import timezone


def get_db_reference(type):
    if type == 'poem':
        return mongo.db.poems
    elif type == 'blog':
        return mongo.db.blogs
    elif type == 'musing':
        return mongo.db.musings
    elif type == 'prompt':
        return mongo.db.prompts


class PostsByUserID(AppResource):

    def __init__(self):
        pass

    def post(self, type, userID):
        # increment plays
        if type == 'blog':
            blogID = request.args['blogID']
            dbRef.update({'_id': ObjectId(blogID)}, {'$inc': {'plays': 1}})
        return {}, 200

    def get(self, type, userID):
        output = []
        posts = get_db_reference(type).find({'userID': userID})
        for i in posts:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200

    def put(self, type, userID):
        # increment views
        if type == 'poem' or type == 'blog':
            postID = request.args['postID']
            posts = get_db_reference(type).find({'_id': ObjectId(postID)},
                                                {'viewedBy': {'$elemMatch': {'$eq': userID}}})
            for i in posts:
                try:
                    app.logger.info(i['viewedBy'])
                except:
                    get_db_reference(type).update({'_id': ObjectId(postID)},
                                                  {'$inc': {'views': 1}, '$addToSet': {'viewedBy': userID}})
        return postID, 200

    def delete(self, type, userID):
        pass
