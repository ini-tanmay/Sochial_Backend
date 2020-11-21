from api.wrap.auth import AppResource
import logging as logger
from app import *
import pymongo
from datetime import timezone

def get_db_reference(type):
    if type == 'poetree':
        return mongo.db.poems
    elif type=='prompt':
        return mongo.db.prompts

def get_db_snippets_reference(type):
    if type == 'poetree':
        return mongo.db.poetree.snippets
    elif type=='prompt':
        return mongo.db.prompts.snippets

class SnippetsByPostID(AppResource):

    def __init__(self):
        pass

    def post(self, postID,type):
        # add a snippet
        snippetDict = request.get_json(force=True)
        # get_db_reference(type).update_one({'_id': ObjectId(postID)}, {'$inc': {'snippets': 1}})
        mongo.db.poetree.snippets.update_one({'_id': ObjectId(postID)},
                                    {'$addToSet': {'snippets': snippetDict}}, upsert=True)
        return {}, 200

    def get(self, postID,type):
        limit = int(request.args['limit'])
        page_no = int(request.args['page_no'])
        snippets = mongo.db.poetree.snippets.find_one({'_id': ObjectId(postID)},
                                             {'snippets': {'$slice': [page_no * limit, (page_no + 1) * limit]}})
        app.logger.info(snippets)
        if snippets is None:
            return [], 200
        if 'snippets' not in snippets:
            return [], 200
        return snippets['snippets'], 200

    def put(self, postID,type):
        # add likes and dislikes
        action = request.args['action']
        timeStamp = int(request.args['ts'])
        userID = request.args['userID']
        if action == 'up':
            get_db_snippets_reference(type).update_one({'$and': [{'snippets.$.dislikedBy': userID}, {'_id': ObjectId(postID)}]},
                                        {'$inc': {"snippets.$.dislikes": -1},
                                         '$pull': {'snippets.$.dislikedBy': userID}})
            get_db_snippets_reference(type).update_one({'$and': [{'_id': ObjectId(postID)}, {"snippets.ts": timeStamp}]},
                                        {'$inc': {"snippets.$.likes": 1},
                                         '$addToSet': {'snippets.$.likedBy': userID}}, upsert=True)
        elif action == 'down':
            get_db_snippets_reference(type).update_one({'$and': [{'snippets.$.likedBy': userID}, {'_id': ObjectId(postID)}]},
                                        {'$inc': {"snippets.$.likes": -1},
                                         '$pull': {'snippets.$.likedBy': userID}})
            get_db_snippets_reference(type).update_one({'$and': [{'_id': ObjectId(postID)}, {"snippets.ts": timeStamp}]},
                                        {'$inc': {"snippets.$.dislikes": 1},
                                         '$addToSet': {'snippets.$.dislikedBy': userID}}, upsert=True)
        return {}, 200

    def delete(self, postID,type):
        # delete the snippet
        timeStamp = int(request.args['ts'])
        snippets = get_db_snippets_reference(type).update_one({'$and': [{'_id': ObjectId(postID)}, {"snippets.ts": timeStamp}]},
                                               {'$pull': {'snippets': {'ts': timeStamp}}})
        return {}, 200
