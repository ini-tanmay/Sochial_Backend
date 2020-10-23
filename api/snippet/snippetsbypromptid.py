from api.wrap.auth import AppResource
import logging as logger
from app import *
import pymongo
from datetime import timezone


class SnippetsByPromptID(AppResource):

    def __init__(self):
        self.snippetsRef = mongo.db.snippets
        pass

    def post(self, promptID):
        # add a snippet
        snippetDict = request.get_json(force=True)
        self.snippetsRef.update({'_id': ObjectId(promptID)},
                                {'$addToSet': {'snippets': snippetDict}}, upsert=True)
        return {}, 200

    def get(self, promptID):
        limit=int(request.args['limit'])
        page_no = int(request.args['page_no'])
        snippets = self.snippetsRef.find_one({'_id': ObjectId(promptID)},
                                             {'snippets': {'$slice': [page_no * limit, (page_no + 1) * limit]}})
        if snippets is None:
            return [],200
        if 'snippets' not in snippets:
            return [],200
        return snippets['snippets'], 200

    def put(self, promptID):
        # add likes and dislikes
        action = request.args['action']
        timeStamp = int(request.args['ts'])
        userID = request.args['userID']
        if action == 'up':
            self.snippetsRef.update_one({'$and': [{'snippets.$.dislikedBy': userID}, {'_id': ObjectId(promptID)}]},
                                        {'$inc': {"snippets.$.dislikes": -1},
                                         '$pull': {'snippets.$.dislikedBy': userID}})
            self.snippetsRef.update_one({'$and': [{'_id': ObjectId(promptID)}, {"snippets.ts": timeStamp}]},
                                        {'$inc': {"snippets.$.likes": 1},
                                         '$addToSet': {'snippets.$.likedBy': userID}}, upsert=True)
        elif action == 'down':
            self.snippetsRef.update_one({'$and': [{'snippets.$.likedBy': userID}, {'_id': ObjectId(promptID)}]},
                                        {'$inc': {"snippets.$.likes": -1},
                                         '$pull': {'snippets.$.likedBy': userID}})
            self.snippetsRef.update_one({'$and': [{'_id': ObjectId(promptID)}, {"snippets.ts": timeStamp}]},
                                        {'$inc': {"snippets.$.dislikes": 1},
                                         '$addToSet': {'snippets.$.dislikedBy': userID}}, upsert=True)

        return {}, 200

    def delete(self, promptID):
        # delete the snippet
        timeStamp = int(request.args['ts'])
        snippets = self.snippetsRef.update_one({'$and': [{'_id': ObjectId(promptID)}, {"snippets.ts": timeStamp}]},
                                               {'$pull': {'snippets': {'ts': timeStamp}}})
        return {}, 200
