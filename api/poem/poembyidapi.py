from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class PoemByID(Resource):

    def __init__(self):
        self.dbRef = mongo.db.poems
        self.commentDbRef = mongo.db.poems.comments

    def post(self, poemID):
        # used to add comments
        commentDict = request.get_json(force=True)
        self.commentDbRef.insert_one(commentDict)
        return {}, 200

    def get(self, poemID):
        output = []
        if poemID == 'userID':
            userID = request.args['user_id']
            poems = self.dbRef.find({'userID': userID})
            for i in poems:
                output.append(i)
        else:
            poem = self.dbRef.find_one({'_id': ObjectId(poemID)})
            return poem, 200
        # gets json and converts it to dict
        if not output:
            return {'result': 'no results lol'}, 200
        return output, 200

    def put(self, poemID):
        c = ObjectId('5f4bc3dce34e386e9c90147c').generation_time
        # used to update poem
        app.logger.info(c.date())
        app.logger.info(c.timetz())
        app.logger.info(c.time())
        app.logger.info(c.now(timezone.utc).timestamp())
        app.logger.info(c.now(timezone.utc).tzname())
        app.logger.info(c.now(timezone.utc).tzinfo())
        return {'result': str(c)}, 200

    def delete(self, poemID):
        logger.debug("Inisde the delete method of PoemByID. PoemID = {}".format(poemId))
        return {"message": "Inside delete method"}, 200
