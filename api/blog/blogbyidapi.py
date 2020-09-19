from flask_restful import Resource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class BlogByID(Resource):

    def __init__(self):
        self.dbRef = mongo.db.blogs

    def get(self, blogID):
        blog = self.dbRef.find_one({'_id': ObjectId(blogID)})
        blog['timeStamp'] = int(ObjectId(blog['_id']).generation_time.timestamp() * 1000)
        return blog, 200

    def put(self, blogID):
        c = ObjectId('5f4bc3dce34e386e9c90147c').generation_time
        # used to update blog
        app.logger.info(c.date())
        app.logger.info(c.timetz())
        app.logger.info(c.time())
        app.logger.info(c.now(timezone.utc).timestamp())
        app.logger.info(c.now(timezone.utc).tzname())
        app.logger.info(c.now(timezone.utc).tzinfo())
        return {'result': str(c)}, 200

    def delete(self, blogID):
        logger.debug("Inisde the delete method of BlogByID. BlogID = {}".format(blogId))
        return {"message": "Inside delete method"}, 200
