from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId # import ObjectId to generate unique ids
from config import MONGODB_URI
import db # import preconfigured database object

user_bp = Blueprint('user', __name__) # create a Blueprint object

# Route for creating a user
@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() # get data from the request
    user = {
        'clerkId': data['clerkId'],
        'email': data['email'],
        'username': data['username'],
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'photo': data['photo']
    }
    result = db.user_collection.insert_one(user) # insert the user into the database
    print(result.inserted_id)
    return jsonify({'message': 'User created successfully!', 'id': str(result.inserted_id)})