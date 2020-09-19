from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class PoemCommentByID(Resource):

    def __init__(self):
        self.commentRef = mongo.db.poems.comments
        self.poemsRef = mongo.db.poems

    def post(self, poemID):
        commentDict = request.get_json(force=True)
        self.poemsRef.update({'_id': ObjectId(poemID)}, {'$inc': {'comments': 1}})
        doc_id = self.commentRef.insert_one(commentDict).inserted_id
        return {'id': doc_id}, 200

    def get(self, poemID):
        output = []
        comments = self.commentRef.find({'postID': poemID}).sort('_id', pymongo.DESCENDING)
        app.logger.info(comments.count())
        for i in comments:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200

    def put(self, poemID):
        pass

    def delete(self, poemID):
        pass
