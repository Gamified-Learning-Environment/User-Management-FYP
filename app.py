from flask import Flask, request, jsonify
from flask_cors import CORS # import CORS for cross-origin resource sharing
import db # import db from db.py

app = Flask(__name__) # Flask constructor takes the name of current module (__name__) as argument

CORS(app) # enable CORS on the app

# test data
data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

@app.route('/')  # route() decorator to tell Flask what URL should trigger the function
def home():
    print("successful connection to User Service")
    return "User Service"

@app.route('/data', methods=['POST'])
def insert_data():
    db.userdb.usercollection.insert_one(data)
    return jsonify("Data inserted successfully" + str(data))

if __name__ == "__main__":
    app.run(debug=True, port=8080)  # run() function of Flask class to run the application on the local development server

# Run the app
# $ python app.py