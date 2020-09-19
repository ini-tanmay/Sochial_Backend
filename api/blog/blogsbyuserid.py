from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class BlogsByUserID(Resource):

    def __init__(self):
        self.dbRef = mongo.db.blogs

    def get(self, userID):
        output = []
        blogs = self.dbRef.find({'userID': userID})
        for i in blogs:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200
