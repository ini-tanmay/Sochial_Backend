import logging as logger
from app import *
import pymongo
from api.wrap.auth import AppResource

def get_db_reference(type):
    if type == 'poem':
        return mongo.db.poems
    elif type == 'blog':
        return mongo.db.blogs
    elif type == 'musing':
        return mongo.db.musings
    elif type == 'prompt':
        return mongo.db.prompts


class Post(AppResource):

    def __init__(self):
        pass

    def post(self, type):
        postDict = request.get_json(force=True)
        doc_id = get_db_reference(type).insert_one(postDict).inserted_id
        return {'id': doc_id}, 200

    def get(self, type):
        # if last id is null return first few items upto the limit
        # if last id is not null return all items from the next item of last id upto the limit
        output = []
        firstDocument = None
        limit = int(request.args['limit'])
        try:
            lastDocumentID = request.args['last_id']
        except:
            firstDocument = (get_db_reference(type).find_one(sort=[('_id', pymongo.ASCENDING)]))
            firstDocument['timeStamp'] = int(ObjectId(firstDocument['_id']).generation_time.timestamp() * 1000)
            return firstDocument,200
        posts = get_db_reference(type).find({'_id': {'$gt': ObjectId((lastDocumentID))}}).sort('_id',
                                                                                               pymongo.ASCENDING).limit(limit)
        for i in posts:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200

    def put(self, type):
        pass
