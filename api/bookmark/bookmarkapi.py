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
        posts = self.dbRef.find({'_id': userID}, {'bookmarkedPosts': {'$slice': [last_no * 30, (last_no + 1) * 30]}})
        for i in posts:
            app.logger.info(i)
            output.append(i['bookmarkedPosts'])
        return output[0], 200
