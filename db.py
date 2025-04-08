from flask import Flask
import pymongo # import pymongo
import os

# Try to import from config, fall back to environment variable if config not available
try:
    from config import MONGODB_URI
except ImportError:
    # When deployed, get from environment variable
    MONGODB_URI = os.environ.get('MONGODB_URI')
    
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI environment variable not set")


client = pymongo.MongoClient(MONGODB_URI) # create a client

userdb = client.get_database('userdatabase') # get the database

user_collection = userdb.usercollection # get the user collection

# Test connection
client.server_info()