from flask import Flask, request, jsonify
from flask_cors import CORS # import CORS for cross-origin resource sharing
import db # import db from db.py
from routes.auth import auth_bp
from config import JWT_SECRET_KEY

app = Flask(__name__) # Flask constructor takes the name of current module (__name__) as argument

CORS(app)

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