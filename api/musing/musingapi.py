from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class Musing(Resource):

    def __init__(self):
        self.dbRef = mongo.db.musings

    def post(self):
        musingDict = request.get_json(force=True)
        doc_id = self.dbRef.insert_one(musingDict).inserted_id
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
        musings = self.dbRef.find({'_id': {'$gt': ObjectId((lastDocumentID))}}).sort('_id', pymongo.ASCENDING).limit(
            limit)
        for i in musings:
            i['timeStamp'] = ObjectId(i['_id']).generation_time.strftime("%Y%m%dT%H%M%SZ")
            output.append(i)

        return output, 200
