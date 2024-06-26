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


class PostByID(AppResource):

    def __init__(self):
        pass

    def post(self, type, postID):
        get_db_reference(type).update({'_id': ObjectId(postID)},
                                      {'$inc': {'awards': 1}, '$addToSet': {'awardedBy': userID}})
        return {}, 200

    def get(self, type, postID):
        post = get_db_reference(type).find_one({'_id': ObjectId(postID)})
        if post is None:
            return 'No post exists'
        post['timeStamp'] = int(ObjectId(post['_id']).generation_time.timestamp() * 1000)
        return post, 200

    def put(self, type, postID):
        req_data = request.get_json(force=True)
        get_db_reference(type).update({'_id': ObjectId(postID)}, {'$set': req_data})
        return {}, 200

    def delete(self, type, postID):
        userID=request.args['userID']
        users=mongo.db.users
        users.update_one({'_id':userID},{'$inc':{'posts':-1}})
        get_db_reference(type).delete_one({'_id': ObjectId(postID)})
        return {}, 200
