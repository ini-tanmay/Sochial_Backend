from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class PostCommentByID(Resource):

    def __init__(self):
        pass

    def post(self, postID, type):
        commentDict = request.get_json(force=True)
        get_db_reference(type).update({'_id': ObjectId(postID)}, {'$inc': {'comments': 1}})
        doc_id = get_commentDB_reference(type).update({'_id': ObjectId(postID)}, {'$push': {'comments': commentDict}},
                                                 upsert=True)

        return {}, 200

    def get(self, postID, type):
        output = []
        comments = []
        last_no = 0
        comments = get_commentDB_reference(type).find({'_id': ObjectId(postID)})
        for i in comments:
            output.append(i)
        return output, 200

    def delete(self, postID, type):
        get_commentDB_reference(type).delete_one({'_id': ObjectId(postID)})
        return {}, 200
