from flask_restful import Resource
import logging as logger
from app import *
import pymongo


def get_db_reference(type):
    if type == 'poem':
        return mongo.db.poems
    elif type == 'blog':
        return mongo.db.blogs
    elif type == 'musing':
        return mongo.db.musings
    elif type == 'prompt':
        return mongo.db.prompts


def get_commentDB_reference(type):
    if type == 'poem':
        return mongo.db.poems.comments
    elif type == 'blog':
        return mongo.db.blogs.comments
    elif type == 'musing':
        return mongo.db.musings.comments
    elif type == 'prompt':
        return mongo.db.prompts.comments


class PostCommentByID(Resource):

    def __init__(self):
        pass

    def post(self, postID, type):
        commentDict = request.get_json(force=True)
        get_db_reference(type).update({'_id': ObjectId(postID)}, {'$inc': {'comments': 1}})
        doc_id = get_commentDB_reference(type).update({'_id': ObjectId(postID)},
                                                      {'$addToSet': {'comments': commentDict}},
                                                      upsert=True)

        return {}, 200

    def get(self, postID, type):
        output = list(get_commentDB_reference(type).find({'_id': ObjectId(postID)}))
        if len(output) == 0:
            return {'_id':'error'}, 200
        for i in output:
            objID = i['_id']
            output = i['comments']
        for i in output:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
        return {'_id': objID, 'comments': output}, 200

    def delete(self, postID, type):
        get_commentDB_reference(type).delete_one({'_id': ObjectId(postID)})
        return {}, 200
