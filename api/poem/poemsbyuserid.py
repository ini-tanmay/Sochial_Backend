from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class PoemsByUserID(Resource):

    def __init__(self):
        self.dbRef = mongo.db.poems

    def get(self, userID):
        output = []
        poems = self.dbRef.find({'userID': userID})
        for i in poems:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200
