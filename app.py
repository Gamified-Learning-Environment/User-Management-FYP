from flask import Flask
from flask import request
from flask import jsonify
import db

app = Flask(__name__) # Flask constructor takes the name of current module (__name__) as argument

@app.route('/')  # route() decorator to tell Flask what URL should trigger the function
def home():
    print("successful connection")
    return "User Service"

#test to insert data to the data base
@app.route("/test")
def test():
    db.db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"

if __name__ == "__main__":
    app.run(debug=True, port=8080)  # run() function of Flask class to run the application on the local development server

# Run the app
# $ python app.py