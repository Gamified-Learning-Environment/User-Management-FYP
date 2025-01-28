from flask import Blueprint, request, jsonify, session 
from werkzeug.security import generate_password_hash, check_password_hash # import password hashing functions
import db # import db
from datetime import datetime
from bson import ObjectId # import ObjectId to generate unique ids

# Blueprint for auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# /register route to create new user in database
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['email', 'password', 'username', 'firstName', 'lastName']
        if not all(field in data for field in required):
            return jsonify({'message': 'Missing required fields'}), 400
            
        # Check if user already exists
        if db.userdb.usercollection.find_one({'email': data['email']}):
            return jsonify({'message': 'User already exists'}), 409
            
        # Create new user
        newUser = {
            'email': data['email'],
            'password': generate_password_hash(data['password']),
            'username': data['username'],
            'firstName': data['firstName'],
            'lastName': data['lastName'],
            'imageUrl': data.get('imageUrl', ''),
            'created_at': datetime.utcnow()
        }
        
        result = db.userdb.usercollection.insert_one(newUser)
        newUser['_id'] = str(result.inserted_id) # Convert ObjectId to string
        
        return jsonify({'message': 'User created successfully', 'user': newUser}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

# /login route to authenticate user
@auth_bp.route('/login', methods=['POST'])
def login(): # get user data from request and check if user exists in database
    try:
        data = request.get_json()

        user = db.userdb.usercollection.find_one({'email': data['email']})
        if not user or not check_password_hash(user['password'], data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        
        # Convert ObjectId to string
        user['_id'] = str(user['_id'])
        session['user'] = user # Save user data in session

        # Return user data if login is successful
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'username': user['username'],
                'firstName': user['firstName'],
                'lastName': user['lastName'],
                'imageUrl': user.get('imageUrl', '')
            }
        }), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
# /logout route to clear session data
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None) # Remove user data from session
    return jsonify({'message': 'Logout successful'}), 200

# /validate route to get user data from session
@auth_bp.route('/checkSession', methods=['GET'])
def checkSession():
    user = session.get('user')
    if user: 
        return jsonify({'user': user}), 200
    return jsonify({'message': 'No active session'}), 401

# /users route to get all users
@auth_bp.route('/users', methods=['GET'])
def get_users():
    users = db.userdb.usercollection.find()
    response = []
    for user in users:
        user['_id'] = str(user['_id'])
        response.append(user)
    return jsonify(response)

# /users/<id> route to get user by id
@auth_bp.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db.userdb.usercollection.find_one({'_id': ObjectId(id)})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

# /users/<id> route to update user by id
@auth_bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    updated_user = {
        'email': data['email'],
        'password': generate_password_hash(data['password']),
        'username': data['username'],
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'imageUrl': data.get('imageUrl', '')
    }
    result = db.userdb.usercollection.update_one({'_id': ObjectId(id)}, {'$set': updated_user})
    if result.modified_count > 0:
        return jsonify({'message': 'User updated successfully'})
    return jsonify({'message': 'User not found'}), 404

# /users/<id> route to delete user by id
@auth_bp.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = db.userdb.usercollection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User not found'}), 404

@auth_bp.route('/preferences', methods=['PUT'])
def update_preferences():
    try: 
        data = request.get_json()
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({'message': 'Unauthorized'}), 401
        
        # update the preferences
        preferences = {
            'quizPreferences': {
                'category': data.get('categories', {}),
                'defaultQuestionCount': data.get('defaultQuestionCount', 5),
            }
        }

        result = db.userdb.usercollection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': preferences}
        )

        if result.modified_count:
            return jsonify({'message': 'Preferences updated successfully'}), 200
        return jsonify({'message': 'Preferences not updated'}), 304
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500


@auth_bp.route('/preferences', methods=['GET'])
def get_preferences():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'message': 'Unauthorized'}), 401
            
        user = db.userdb.usercollection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'message': 'User not found'}), 404
            
        return jsonify(user.get('quizPreferences', {
            'categories': {},
            'defaultQuestionCount': 5
        })), 200
        
    except Exception as e:
        return jsonify({'message': str(e)}), 500