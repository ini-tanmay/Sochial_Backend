from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class PromptByID(Resource):

    def __init__(self):
        self.dbRef = mongo.db.prompts

    def get(self, promptID):
        prompt = self.dbRef.find_one({'_id': ObjectId(promptID)})
        prompt['timeStamp'] = ObjectId(prompt['_id']).generation_time.timestamp() * 1000
        return prompt, 200

    def put(self, promptID):
        c = ObjectId('5f4bc3dce34e386e9c90147c').generation_time
        # used to update prompt
        app.logger.info(c.date())
        app.logger.info(c.timetz())
        app.logger.info(c.time())
        app.logger.info(c.now(timezone.utc).timestamp())
        app.logger.info(c.now(timezone.utc).tzname())
        app.logger.info(c.now(timezone.utc).tzinfo())
        return {'result': str(c)}, 200

    def delete(self, promptID):
        logger.debug("Inisde the delete method of PromptByID. PromptID = {}".format(promptID))
        return {"message": "Inside delete method"}, 200
