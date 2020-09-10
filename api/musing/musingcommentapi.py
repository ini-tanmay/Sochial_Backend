from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class MusingCommentByID(Resource):

    def __init__(self):
        self.commentRef = mongo.db.musings.comments
        self.musingsRef=mongo.db.musings

    def post(self, musingID):
        commentDict = request.get_json(force=True)
        self.musingsRef.update({'_id':ObjectId(musingID)},{'$inc':{'comments':1}})
        doc_id = self.commentRef.insert_one(commentDict).inserted_id
        return {'id': doc_id}, 200

    def get(self, musingID):
        output = []
        comments = self.commentRef.find({'postID': musingID}).sort('_id', pymongo.DESCENDING)
        app.logger.info(comments.count())
        for i in comments:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200

    def put(self, musingID):
        pass

    def delete(self, musingID):
        pass
