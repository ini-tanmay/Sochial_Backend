from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class PromptsByUserID(Resource):

    def __init__(self):
        self.dbRef = mongo.db.prompts

    def get(self, userID):
        output = []
        prompts = self.dbRef.find({'userID': userID})
        for i in prompts:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200
