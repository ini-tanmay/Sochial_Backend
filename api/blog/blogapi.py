from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class Blog(Resource):

    def __init__(self):
        self.dbRef = mongo.db.blogs

    def post(self):
        blogDict = request.get_json(force=True)
        doc_id = self.dbRef.insert_one(blogDict).inserted_id
        return {'id': doc_id}, 200

    def get(self):
        output = []
        lastDocument = None
        limit = int(request.args['limit'])
        try:
            lastDocumentID = request.args['last_id']
        except Exception as e:
            lastDocument = self.dbRef.find_one(sort=[('_id', pymongo.ASCENDING)])

        if lastDocument is not None:
            lastDocumentID = lastDocument.get('_id')
            app.logger.info(lastDocumentID)
        if lastDocument is not None:
            lastDocument['timeStamp'] = int(ObjectId(lastDocument['_id']).generation_time.timestamp() * 1000)
            output.append(lastDocument)
        else:
            return [], 200
        blogs = self.dbRef.find({'_id': {'$gt': ObjectId((lastDocumentID))}}).sort('_id', pymongo.ASCENDING).limit(
            limit)
        for i in blogs:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200
