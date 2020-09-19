from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class BlogCommentByID(Resource):

    def __init__(self):
        self.commentRef = mongo.db.blogs.comments
        self.blogsRef = mongo.db.blogs

    def post(self, blogID):
        commentDict = request.get_json(force=True)
        self.blogsRef.update({'_id': ObjectId(blogID)}, {'$inc': {'comments': 1}})
        doc_id = self.commentRef.insert_one(commentDict).inserted_id
        return {'id': doc_id}, 200

    def get(self, blogID):
        output = []
        comments = self.commentRef.find({'postID': blogID}).sort('_id', pymongo.DESCENDING)
        app.logger.info(comments.count())
        for i in comments:
            i['timeStamp'] = int(ObjectId(i['_id']).generation_time.timestamp() * 1000)
            output.append(i)
        return output, 200

    def put(self, blogID):
        pass

    def delete(self, blogID):
        pass
