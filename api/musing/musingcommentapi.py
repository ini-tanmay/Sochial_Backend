from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class MusingCommentByID(Resource):

    def __init__(self):
        self.commentRef = mongo.db.musings.comments

    def post(self, musingID):
        commentDict = request.get_json(force=True)
        doc_id = self.commentRef.insert_one(commentDict).inserted_id
        return {'id': doc_id}, 200

    def get(self, musingID):
        output = []
        comments = self.commentRef.find({'_id': ObjectID(musingID)}).sort('_id', pymongo.DESCENDING)
        app.logger.info(comments.count())
        for i in comments:
            output.append(i)
        return output, 200

    def put(self, musingID):
        pass

    def delete(self, musingID):
        pass
