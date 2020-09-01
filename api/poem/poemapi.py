from flask_restful import Resource
import logging as logger
from app import *
import pymongo

class Poem(Resource):

    def __init__(self):
        self.dbRef=mongo.db.poems

    def post(self):
        poemDict=request.get_json(force=True)
        self.commentDbRef.insert_one(poemDict).inserted_id
        return {}, 200

    def get(self):
        output = []
        lastDocument = None
        limit=int(request.args['limit'])
        try:
            lastDocumentID=request.args['last_id']
        except Exception as e:
            lastDocument = self.dbRef.find_one(sort=[('timeStamp', pymongo.DESCENDING)])
            lastDocumentID = lastDocument.get('_id')
        if lastDocument is not None:
            output.append(lastDocument)
        poems = self.dbRef.find({'_id': {'$lt': ObjectId((lastDocumentID))}}).sort('timeStamp',
                                                                                   pymongo.DESCENDING).limit(limit)
        for i in poems:
            output.append(i)
        return output, 200

