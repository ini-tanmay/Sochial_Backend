from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class Prompt(Resource):

    def __init__(self):
        self.dbRef = mongo.db.prompts
        self.commentRef = mongo.db.prompts.comments

    def post(self):
        promptDict = request.get_json(force=True)
        doc_id = self.d.insert_one(promptDict).inserted_id
        return {'id': doc_id}, 200

    def get(self):
        output = []
        lastDocument = None
        limit = int(request.args['limit'])
        try:
            lastDocumentID = request.args['last_id']
        except Exception as e:
            lastDocument = self.dbRef.find_one(sort=[('_id', pymongo.ASCENDING)])
            lastDocumentID = lastDocument.get('_id')
            app.logger.info(lastDocumentID)
        if lastDocument is not None:
            output.append(lastDocument)
        prompts = self.dbRef.find({'_id': {'$gt': ObjectId((lastDocumentID))}}).sort('_id', pymongo.ASCENDING).limit(
            limit)
        for i in prompts:
            i['timeStamp'] = ObjectId(i['_id']).generation_time.timestamp()*1000
            output.append(i)
        return output, 200
