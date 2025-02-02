from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash # import password hashing functions
import db # import db
from datetime import datetime
from bson import ObjectId # import ObjectId to generate unique ids
from flask import session

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
        
        #if not user or not check_password_hash(user['password'], data['password']):
            #return jsonify({'message': 'Invalid credentials'}), 401
        
        if user and check_password_hash(user['password'], data['password']):
             # Store only necessary user info in session
            session['user'] = {
                '_id': str(user['_id']),
                'email': user['email'],
                'username': user['username']
            }
            session.permanent = True

            return jsonify({ # return user data if login is successful
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
        
        return jsonify({'message': 'Invalid credentials'}), 401
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
# /logout route to clear session data and handle CORS preflight
@auth_bp.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return jsonify({'message': 'OK'}), 200
        
    try:
        # Clear session
        session.clear()
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        print(f"Error in logout: {str(e)}")
        return jsonify({'message': 'Error during logout'}), 500
    
# /verify route to check if user is logged in
@auth_bp.route('/verify', methods=['GET'])
def verify_session():
    try:
        if 'user' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
            
        user_id = session['user'].get('_id')
        if not user_id:
            print("Invalid user data in session")  # Debug logging
            return jsonify({'message': 'Invalid session'}), 401
            
        user_data = session.get('user')
        if not user_data or '_id' not in user_data:
            print("Invalid user data in session")  # Debug logging
            return jsonify({'message': 'Invalid session'}), 401
            
        # Return success with user data
        return jsonify({
            'message': 'Session valid',
            'user': user_data
        }), 200
        
    except Exception as e:
        print(f"Error verifying session: {str(e)}")
        return jsonify({'message': 'Server error'}), 500

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

# /preferences route to update user preferences
@auth_bp.route('/preferences', methods=['PUT'])
def update_preferences():
    try: 
        data = request.get_json()
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({'message': 'Unauthorized'}), 401
        
        try:
            object_id = ObjectId(user_id)
        except:
            return jsonify({'message': 'Invalid user id format'}), 400
        
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

# /preferences route to get user preferences
@auth_bp.route('/preferences', methods=['GET'])
def get_preferences():
    try:
        # Explicitly check if user is logged in
        if 'user_id' not in session:
            return jsonify({'message': 'Unauthorized - Please log in'}), 401
        
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'message': 'Unauthorized'}), 401
        
        # Get user preferences, create default if none exist
        user = db.userdb.usercollection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'message': 'User not found'}), 404
            
        # Return default preferences if none exist
        preferences = user.get('preferences', {
            'quizPreferences': {
                'category': {},
                'defaultQuestionCount': 5
            }
        })
            
        return jsonify(preferences), 200
        
    except Exception as e:
        print(f"Error in get_preferences: {str(e)}")  # Add logging
        return jsonify({'message': str(e)}), 500