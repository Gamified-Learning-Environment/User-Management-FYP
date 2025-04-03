from flask import Flask, session, request, jsonify
from flask_cors import CORS # import CORS
from flask_session import Session # import for session management
import db # import db
from routes.auth import auth_bp
from datetime import timedelta
import os

app = Flask(__name__) # Flask app instance

# Configure session to store data in filesystem of server
#app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SECRET_KEY'] = 'UserSess7274' 
#app.config['SESSION_COOKIE_HTTPONLY'] = True # Prevent client-side access to session cookie
#app.config['SESSSION_COOKIE_SECURE'] = False # Ensure session cookie is sent only over HTTPS, set True in production
#app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # Mitigate CSRF attacks
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7) # Set session lifetime to 30 minutes
#app.config['SESSION_COOKIE_NAME'] = 'UserSession' # Set session cookie name
#Session(app) # Initialize Session

#CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True, allow_headers=['Content-Type', 'Authorization'], methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']) # Enable CORS on all routes and allow credentials

app.config.update(
    SECRET_KEY='UserSess7274',
    SESSION_TYPE='filesystem',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    SESSION_COOKIE_SECURE=False,  # Set to True in production
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_NAME='quizapp_session',
    SESSION_COOKIE_DOMAIN=None,  # Add this for local development
    SESSION_REFRESH_EACH_REQUEST=True  # Keep session alive
)

# Initialize session
Session(app)

CORS(app, 
    resources={
        r"/api/*": {
            #"origins": ["http://localhost:3000"],
            "origins": os.environ.get('CORS_ORIGINS', '*').split(','),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "cookie"],
            "expose_headers": ["Content-Type", "Authorization", "Set-Cookie"],
            "supports_credentials": True,
            "allow_credentials": True
        }
    }
)

# Register blueprints
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True, port=8080)

# test data
data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Test route to check if service runs
@app.route('/') 
def home():
    print("successful connection to User Service")
    return "User Service"

# Test route to insert data into MongoDB
@app.route('/data', methods=['POST'])
def insert_data():
    db.userdb.usercollection.insert_one(data)
    return jsonify("Data inserted successfully" + str(data))



if __name__ == "__main__":
    app.run(debug=True, port=8080) 

# Run the app
# $ python app.py