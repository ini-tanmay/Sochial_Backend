from api.wrap.auth import AppResource
import logging as logger
from firebase_admin import auth
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


class CommentReplyByID(AppResource):

    def __init__(self):
        pass

    def put(self, postID, type, timeStamp):
        # rts=int(request.args['rts'])
        # action= 'like' #(request.args['action'])
        # if action=='like':
        #     get_commentDB_reference(type).update_one({'$and':[{'_id':ObjectId(postID)}, {"comments.ts":timeStamp },{'comments.$.replies.ts':rts}]}, {'$inc': {"comments.$.replies.likes": 1},'addToSet':{'comments.$[].replies.likedBy'}})
        # elif action=='dislike':
        #     get_commentDB_reference(type).update_one({'$and': [{'_id': ObjectId(postID)}, {"comments.ts": timeStamp}]},
        #                                              {'$inc': {"comments.$.likes": -1}})
        return {}, 200

    def post(self, postID, type, timeStamp):
        commentDict = request.get_json(force=True)
        otherFcmToken = request.args['server_log']
        app.logger.info(commentDict)
        app.logger.info(postID)
        app.logger.info(type)
        app.logger.info(timeStamp)
        get_db_reference(type).update_one({'_id': ObjectId(postID)}, {'$inc': {'comments': 1}})
        doc_id = get_commentDB_reference(type).update_one(
            {'$and': [{'_id': ObjectId(postID)}, {"comments.ts": timeStamp}]},
            {'$addToSet': {'comments.$.replies': commentDict}},
            upsert=True)
        headers = request.headers
        decoded_token = auth.verify_id_token(headers['Authorization'])
        uid = decoded_token['uid']
        if commentDict['userID']!=uid:
            NotificationService().send_custom_message(otherFcmToken,
                                                  '@' + commentDict['usern'] + ' replied to your comment',
                                                  commentDict['text'][0:max(len(commentDict['text']), 50)] + '...')
        return {}, 200

    def delete(self, postID, type, timeStamp):
            app.logger.info(timeStamp)
            app.logger.info(postID)
            app.logger.info(type)
            rts = int(request.args['rts'])
            app.logger.info(rts)
            get_db_reference(type).update_one({'_id': ObjectId(postID)}, {'$inc': {'comments': -1}})
            get_commentDB_reference(type).update_one({'$and': [{'_id': ObjectId(postID)}, {"comments.ts": timeStamp}]},
                                                     {'$pull': {'comments.$.replies': {'ts': rts}}})
            return {}, 200
