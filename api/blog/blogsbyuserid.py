from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class BlogsByUserID(Resource):

    def __init__(self):
        self.dbRef = mongo.db.blogs

    def post(self, userID):
        # increment views
        blogID = request.args['blogID']
        e = self.dbRef.find({'_id': ObjectId(blogID)}, {'viewedBy': {'$elemMatch': {'$eq': userID}}})
        for i in e:
            try:
                app.logger.info(i['viewedBy'])
            except:
                self.dbRef.update({'_id': ObjectId(blogID)}, {'$inc': {'views': 1}, '$push': {'viewedBy': userID}})

        return blogID, 200

    def get(self, userID):
        output = []
        blogs = self.dbRef.find({'userID': userID})
        for i in blogs:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200

    def put(self, userID):
        # increment plays
        blogID = request.args['blogID']
        dbRef.update({'_id': ObjectId(blogID)}, {'$inc': {'plays': 1}})
