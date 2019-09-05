from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION

client = MongoClient()
client = MongoClient(MONGO_HOST, MONGO_PORT, connect=False)
db     = client[MONGO_DB]



