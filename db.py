from flask import Flask
import pymongo # import pymongo
from config import MONGODB_URI


client = pymongo.MongoClient(MONGODB_URI) # create a client

userdb = client.get_database('userdatabase') # get the database

user_collection = userdb.usercollection # get the user collection

# Test connection
client.server_info()