from api.wrap.auth import AppResource
import logging as logger
from app import *
import pymongo


class Bookmark(AppResource):

    def __init__(self):
        self.dbRef = mongo.db.bookmarks

    def post(self, userID):
        bookmarkDict = request.get_json(force=True)
        app.logger.info(bookmarkDict)
        self.dbRef.update_one({'_id': (userID)},
                              {'$addToSet': {'bookmarkedPosts': bookmarkDict}},
                              upsert=True)
        return {}, 200

    def get(self, userID):
        bookmarks = self.dbRef.find_one({'_id': userID})
        if bookmarks is None:
            return [], 200
        if 'bookmarkedPosts' not in bookmarks:
            return [], 200
        return bookmarks['bookmarkedPosts'], 200

    def delete(self, userID):
        postID = request.args['postID']
        self.dbRef.update_one({'_id': (userID)},
                              {'$pull': {'bookmarkedPosts': {'postID': (postID)}}},
                              )
        return {}, 200
