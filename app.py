from flask import Flask, session, request, jsonify
from flask_cors import CORS # import CORS
from flask_session import Session # import for session management
import db # import db
from routes.auth import auth_bp

app = Flask(__name__) # Flask app instance

# Configure session to store data in filesystem of server
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'UserSess7274' 
app.config['SESSION_COOKIE_HTTPONLY'] = True # Prevent client-side access to session cookie
app.config['SESSSION_COOKIE_SECURE'] = False # Ensure session cookie is sent only over HTTPS, set True in production

Session(app) # Initialize Session

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True) # Enable CORS on all routes and allow credetials

# Register blueprints
app.register_blueprint(auth_bp)

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