from flask import Flask
import pymongo # import pymongo
from app import app


CONNECTION_STRING = "mongodb+srv://ExperAdmin:727476@cluster0.kr7hf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(CONNECTION_STRING) # create a MongoClient object
db = client.get_database('userdatabase') # get the database
user_collection = db.usercollection # get the collection

# Test connection
client.server_info()
