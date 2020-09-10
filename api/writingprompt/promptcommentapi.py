from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class PromptCommentByID(Resource):

    def __init__(self):
        self.commentRef = mongo.db.prompts.comments
        self.promptsRef=mongo.db.prompts

    def post(self, promptID):
        commentDict = request.get_json(force=True)
        self.promptsRef.update({'_id':ObjectId(promptID)},{'$inc':{'comments':1}})
        doc_id = self.commentRef.insert_one(commentDict).inserted_id
        return {}, 200

    def get(self, promptID):
        output = []
        comments = self.commentRef.find({'postID': promptID}).sort('_id', pymongo.DESCENDING)
        app.logger.info(comments.count())
        for i in comments:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200

    def put(self, promptID):
        pass

    def delete(self, promptID):
        pass
