from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class MusingsByUserID(Resource):

    def __init__(self):
        self.dbRef = mongo.db.musings

    def get(self, userID):
        output = []
        musings = self.dbRef.find({'userID': userID})
        for i in musings:
            i['timeStamp'] = ObjectId(i['_id']).generation_time.strftime("%Y%m%dT%H%M%SZ")
            output.append(i)
        return output, 200
