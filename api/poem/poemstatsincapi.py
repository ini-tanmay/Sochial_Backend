# from flask_restful import Resource
# import logging as logger
# from app import *
# import pymongo
#
#
# class PoemStatsIncByID(Resource):
#
#     def __init__(self):
#         self.dbRef = mongo.db.poems
#
#     def put(self, poemID):
#         parameters = list(request.args.getlist('parameters'))
#         to_be_updated_params = dict.fromkeys(parameters, 1)
#         x = self.dbRef.update({'_id': ObjectId(poemID)}, {'$inc': to_be_updated_params},
#                               upsert=False, multi=True)
#         # used to increment likes, comments, awards, views
#         # userID = request.args['username']
#         # bio = request.args['bio']
#         # fcm
#         # userID = request.args['name']
#         # websiteLink = request.args['websiteLink']
#         # x = self.dbRef.update({'_id': ObjectId(poemID)}, {'$inc': {'likes': 1, 'views': 1, 'comments': 0, 'awards': 0}})
#         logger.debug("Inisde the put method of PoemByID. PoemID = {}".format(poemID))
#         return {"message": "Inside put method of PoemById. PoemID = {}".format(poemID), "s": str(x)}, 200
