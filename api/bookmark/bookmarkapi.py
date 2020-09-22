from flask_restful import Resource
import logging as logger
from app import *
import pymongo


class Bookmark(Resource):

    def __init__(self):
        self.dbRef = mongo.db.bookmarks

    # title
    # photo id
    # text
    # timestamp
    # type

    def post(self, userID):
        bookmarkDict = request.get_json(force=True)
        self.dbRef.update_one({'_id': (userID)},
                              {'$push': {'bookmarkedPosts': bookmarkDict}},
                              upsert=True)
        return {'id': 'true'}, 200

    def get(self, userID):
        last_no = 0
        output = []
        posts = self.dbRef.find({'_id': userID})
        for i in posts:
            app.logger.info(i)
            try:
                app.logger.info(i['bookmarkedPosts'])
                output.append(i['bookmarkedPosts'])
            except:
                return {}, 365
        if posts.count()<=0:
            return {}, 365
        return output[0], 200
