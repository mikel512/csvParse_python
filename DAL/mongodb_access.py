import pymongo
from pymongo import MongoClient


class MongoDbAccess:
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://<username>:<password>@cluster0.2n2ic.azure.mongodb.net/test?authSource=admin&replicaSet=atlas-h8flgp-shard-0&readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=true")

    def post_single_doc(self, json_post, post_id):
        db = self.cluster["sba_data"]
        collection = db["sba"]
        print('Inserting doc into mongoDB:')
        try:
            post = { "_id" : post_id, "content" : json_post}
            collection.insert_one(post)
        except Exception as e:
            print(e)
