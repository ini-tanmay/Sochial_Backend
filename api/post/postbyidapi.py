from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone
from api.shared import *


class PostByID(Resource):

    def __init__(self):
        pass

    def post(self, type, postID):
        get_db_reference(type).update({'_id': ObjectId(postID)},
                                      {'$inc': {'awards': 1}, '$push': {'awardedBy': userID}})
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
        get_db_reference(type).delete_one({'_id': ObjectId(postID)})
        return {}, 200
