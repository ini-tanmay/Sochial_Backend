from api.wrap.auth import AppResource
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


class PostCommentByID(AppResource):

    def __init__(self):
        pass

    def post(self, postID, type):
        commentDict = request.get_json(force=True)
        get_db_reference(type).update_one({'_id': ObjectId(postID)}, {'$inc': {'comments': 1}})
        doc_id = get_commentDB_reference(type).update_one({'_id': ObjectId(postID)},
                                                      {'$addToSet': {'comments': commentDict}},
                                                      upsert=True)

        return {}, 200

    def get(self, postID, type):
        output=[]
        comments = list(get_commentDB_reference(type).find({'_id': ObjectId(postID)}))
        if len(comments) == 0:
            return [], 200
        for i in comments:
            output = i['comments']
        return output, 200

    def delete(self, postID, type):
        get_commentDB_reference(type).delete_one({'_id': ObjectId(postID)})
        return {}, 200
