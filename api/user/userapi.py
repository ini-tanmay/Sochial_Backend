from api.wrap.auth import AppResource
import logging as logger
from app import *
import json


class User(AppResource):

    def __init__(self):
        self.dbRef = mongo.db.users

    def post(self, userID):
        # _id field will be added in post json data
        req_data = request.get_json(force=True)
        self.dbRef.insert_one(req_data)
        return {}, 200

    def get(self, userID):
        user = self.dbRef.find_one({'_id': userID})
        if user is None:
            return None, 200
        return user, 200

    def put(self, userID):
        req_data = request.get_json(force=True)
        self.dbRef.update({'_id': userID}, {'$set': req_data})
        return {"message": userID}, 200

    def delete(self, userID):
        logger.debug("Inisde the delete method of Task")
        return {"message": "Inside delete method"}, 200
