from flask import Blueprint, request, jsonify
# werkzeug is used to hash passwords securely and check them
from werkzeug.security import generate_password_hash, check_password_hash
import db
from datetime import datetime

# Blueprint for auth routes
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# /register route to create new user in database
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required = ['email', 'password', 'username', 'firstName', 'lastName']
    if not all(field in data for field in required):
        return jsonify({'message': 'Missing required fields'}), 400
        
    # Check if user already exists
    if db.userdb.usercollection.find_one({'email': data['email']}):
        return jsonify({'message': 'User already exists'}), 409
        
    # Create new user
    new_user = {
        'email': data['email'],
        'password': generate_password_hash(data['password']),
        'username': data['username'],
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'imageUrl': data.get('imageUrl', ''),
        'created_at': datetime.utcnow()
    }
    
    result = db.userdb.usercollection.insert_one(new_user)
    
    return jsonify({'message': 'User created successfully', 'user': new_user}), 201

# /login route to authenticate user
@auth_bp.route('/login', methods=['POST'])
def login(): # get user data from request and check if user exists in database
    data = request.get_json()
    
    user = db.userdb.usercollection.find_one({'email': data['email']})
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
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