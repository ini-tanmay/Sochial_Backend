from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class MusingByID(Resource):

    def __init__(self):
        self.dbRef = mongo.db.musings

    def get(self, musingID):
        musing = self.dbRef.find_one({'_id': ObjectId(musingID)})
        musing['timeStamp'] = ObjectId(musing['_id']).generation_time.strftime("%Y%m%dT%H%M%SZ")
        return musing, 200

    def put(self, musingID):
        c = ObjectId('5f4bc3dce34e386e9c90147c').generation_time
        # used to update musing
        app.logger.info(c.date())
        app.logger.info(c.timetz())
        app.logger.info(c.time())
        app.logger.info(c.now(timezone.utc).timestamp())
        app.logger.info(c.now(timezone.utc).tzname())
        app.logger.info(c.now(timezone.utc).tzinfo())
        return {'result': str(c)}, 200

    def delete(self, musingID):
        logger.debug("Inisde the delete method of MusingByID. MusingID = {}".format(musingID))
        return {"message": "Inside delete method"}, 200
