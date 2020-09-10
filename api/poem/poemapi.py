from flask_restful import Resource
import logging as logger
from app import *
import pymongo

class Poem(Resource):

    def __init__(self):
        self.dbRef=mongo.db.poems

    def post(self):
        poemDict=request.get_json(force=True)
        doc_id = self.dbRef.insert_one(poemDict).inserted_id
        return {'id': doc_id}, 200

    def get(self):
        output = []
        lastDocument = None
        limit=int(request.args['limit'])
        try:
            lastDocumentID=request.args['last_id']
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
        poems = self.dbRef.find({'_id': {'$gt': ObjectId((lastDocumentID))}}).sort('_id', pymongo.ASCENDING).limit(
            limit)
        for i in poems:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200

    # def put(self):
    #     limit=int(request.args['limit'])
    #     lastDocumentID=request.args['last_id']
    #
    #     postIDs = []
    #     poems = []
    #     scores = []
    #     poemsRef = mongo.db.poems
    #     config = {
    #         "apiKey": "AIzaSyCbxuL2byX9tLgXrS7muw5kwGE5zl9-eM0",
    #         "authDomain": "sochial-ee116.firebaseapp.com",
    #         "databaseURL": "https://sochial-ee116.firebaseio.com",
    #         'storageBucket': ''
    #     }
    #     firebase = pyrebase.initialize_app(config)
    #     db = firebase.database()
    #     result = db.child("posts").child('poems').order_by_child("likeCount").limit_to_first(100).get()
    #     for key, val in result.val().items():
    #         postIDs.append(key)
    #         if val['viewCount'] is None:
    #             val['viewCount'] = 1
    #         scores.append(get_score(val['likeCount'], val['viewCount']))
    #     all_posts = dict(zip(postIDs, scores))
    #     all_posts = dict(sorted(all_posts.items(), key=lambda x: x[1], reverse=True))
    #     for key, val in all_posts.items():
    #         poem = poemsRef.find_one({'_id': ObjectId(key)})
    #         poems.append(poem)
    #     return jsonify(poems)
