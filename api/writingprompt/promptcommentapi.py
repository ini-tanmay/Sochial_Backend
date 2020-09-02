from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class PromptCommentByID(Resource):

    def __init__(self):
        self.commentRef = mongo.db.prompts.comments

    def post(self, promptID):
        commentDict = request.get_json(force=True)
        doc_id = self.commentRef.insert_one(commentDict).inserted_id
        return {'id': doc_id}, 200

    def get(self, promptID):
        output = []
        comments = self.commentRef.find({'_id': ObjectId(promptID)}).sort('_id', pymongo.DESCENDING)
        app.logger.info(comments.count())
        for i in comments:
            output.append(i)
        return output, 200

    def put(self, promptID):
        pass

    def delete(self, promptID):
        pass
