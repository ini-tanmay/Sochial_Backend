# from flask_restful import Resource
# import logging as logger
# from app import *
# import pymongo
#
#
# class PoemStatsDecrByID(Resource):
#
#     def __init__(self):
#         self.dbRef = mongo.db.poems
#
#     def put(self, poemID):
#         parameters = list(request.args.getlist('parameters'))
#         to_be_updated_params = dict.fromkeys(parameters, -1)
#         x = self.dbRef.update({'_id': ObjectId(poemID)}, {'$inc': to_be_updated_params},
#                               upsert=False, multi=True)
#         logger.debug("Inisde the put method of PoemByID. PoemID = {}".format(poemID))
#         return {"message": "Inside put method of PoemById. PoemID = {}".format(poemID), "s": str(x)}, 200
