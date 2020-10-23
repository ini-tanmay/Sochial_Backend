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


    # def put(self, postID, type):
    #     timeStamp = int(request.args['ts'])
    #     userID = int(request.args['userID'])
    #     action = (request.args['action'])
    #     if action == 'up':
    #         get_commentDB_reference(type).update_one({'$and': [{'_id': ObjectId(postID)}, {"comments.ts": timeStamp}]},
    #                                                  {'$inc': {"comments.$.likes": 1},
    #                                                   '$addToSet': {'likedBy': userID}})
    #     elif action == 'down':
    #         get_commentDB_reference(type).update_one({'$and': [{'_id': ObjectId(postID)}, {"comments.ts": timeStamp}]},
    #                                                  {'$inc': {"comments.$.likes": -1},
    #                                                   '$addToSet': {'likedBy': userID}})
    #     return {}, 200


class PostCommentByID(AppResource):

    def __init__(self):
        pass

    def put(self, postID, type):
        timeStamp = int(request.args['ts'])
        userID = (request.args['userID'])
        get_commentDB_reference(type).update_one({'$and': [{'_id': ObjectId(postID)}, {"comments.ts": timeStamp}]},
                                                     {'$inc': {"comments.$.likes": 1},
                                                      '$addToSet': {'comments.$.likedBy': userID}},upsert=True)
        return {}, 200

    def post(self, postID, type):
        commentDict = request.get_json(force=True)
        get_db_reference(type).update_one({'_id': ObjectId(postID)}, {'$inc': {'comments': 1}})
        doc_id = get_commentDB_reference(type).update_one({'_id': ObjectId(postID)},
                                                          {'$addToSet': {'comments': commentDict}},
                                                          upsert=True)
        return {}, 200

    def get(self, postID, type):
        output = []
        comments = get_commentDB_reference(type).find_one({'_id': ObjectId(postID)})
        if comments is None:
            return [],200
        if 'comments' not in comments:
            return [],200
        return comments['comments'], 200
