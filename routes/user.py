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

# Route for getting all users
@user_bp.route('/users', methods=['GET']) 
def get_users():
    users = db.user_collection.find()
    response = []
    for user in users:
        user['_id'] = str(user['_id'])
        response.append(user)
    return jsonify(response)

# Route for getting a user by id
@user_bp.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.user_collection.find_one({'_id': ObjectId(id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

# Route for updating a user
@user_bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    updated_user = {
        'clerkId': data['clerkId'],
        'email': data['email'],
        'username': data['username'],
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'photo': data['photo']
    }
    result = db.user_collection.update_one({'_id': ObjectId(id)}, {'$set': updated_user})
    if result.modified_count > 0:
        return jsonify({'message': 'User updated successfully'})
    return jsonify({'message': 'User not found'}), 404