import os
from pymongo import MongoClient
from .base import BaseConnector

class MongoConnector(BaseConnector):
    def __init__(self, db_uri=None, db_name=None):
        self.db_uri = db_uri or os.environ.get("MONGO_URI")
        self.db_name = db_name or os.environ.get("MONGO_DB_NAME")

    def get_connection(self):
        client = MongoClient(self.db_uri)
        db = client[self.db_name]
        return db
