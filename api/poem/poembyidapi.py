from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class PoemByID(Resource):

    def __init__(self):
        self.dbRef = mongo.db.poems



    def get(self, poemID):
        poem = self.dbRef.find_one({'_id': ObjectId(poemID)})
        poem['timeStamp'] = int(ObjectId(poem['_id']).generation_time.timestamp() * 1000)
        return poem, 200

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

