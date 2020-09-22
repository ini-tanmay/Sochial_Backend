from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class PostCommentByID(Resource):

    def __init__(self):
        self.poemCommentsRef = mongo.db.poems.comments
        self.blogCommentsRef = mongo.db.blogs.comments
        self.promptCommentsRef = mongo.db.prompts.comments
        self.musingCommentsRef = mongo.db.musings.comments
        self.postsRef = mongo.db.posts

    def post(self, postID, type):
        commentDict = request.get_json(force=True)
        self.postsRef.update({'_id': ObjectId(postID)}, {'$inc': {'comments': 1}})
        if type == 'poem':
            doc_id = self.poemCommentsRef.update({'_id': ObjectId(postID)}, {'$push': {'comments': commentDict}},upsert=True)
        if type == 'blog':
            doc_id = self.blogCommentsRef.update({'_id': ObjectId(postID)}, {'$push': {'comments': commentDict}},upsert=True)
        if type == 'musing':
            doc_id = self.musingCommentsRef.update({'_id': ObjectId(postID)}, {'$push': {'comments': commentDict}},upsert=True)
        if type == 'prompt':
            doc_id = self.promptCommentsRef.update({'_id': ObjectId(postID)}, {'$push': {'comments': commentDict}},upsert=True)
        return {'id': 'tt'}, 200

    def get(self, postID, type):
        output = []
        comments=[]
        last_no=0
        if type == 'poem':
            comments = self.poemCommentsRef.find({'_id': ObjectId(postID)})
        if type == 'blog':
            comments = self.blogCommentsRef.find({'_id': ObjectId(postID)})
        if type == 'musing':
            comments = self.musingCommentsRef.find({'_id': ObjectId(postID)})
        if type == 'prompt':
            comments = self.promptCommentsRef.find({'_id': ObjectId(postID)})
        for i in comments:
            output.append(i)
        return output, 200

    def put(self, postID, type):
        pass

    def delete(self, postID, type):
        pass
