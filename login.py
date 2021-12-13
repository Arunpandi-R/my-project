from os import access
from typing import get_origin
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
import datetime
import random
import string
import time

# Making a Connection with MongoClient
my_clint = MongoClient("mongodb://localhost:27017/")
# database
dbrs = my_clint["app_database"]
# collection
user_information = dbrs["User"]

app = Flask(__name__)
jwt = JWTManager(app)

# JWT Config
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"


@app.route("/dashboard")
@jwt_required
def dasboard():
    return jsonify(message="Welcome! to the Data Science Learner")


@app.route("/signup", methods=["POST"])
def rsig():
    email_id = request.form["email_id"]
    # test = User.query.filter_by(email=email).first()
    test = user_information.find_one({"email_id": email_id})
    if test:
        return jsonify(message="User Already Exist")
    else:
        username = request.form["username"]
        password = request.form["password"]
        user_info = dict(username=username, email_id=email_id, password=password)
        user_information.insert_one(user_info)
        return jsonify(message="User added sucessfully")


@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        email_id = request.json["email_id"]
        password = request.json["password"]
    else:
        email_id = request.form["email_id"]
        password = request.form["password"]

    test = user_information.find_one({"email_id": email_id, "password": password})
    if test:
        access_token=create_access_token(identity=email_id)
        return jsonify(message="Login Succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad Email or Password")


if __name__ == '__main__':
    app.run(port=80, debug=True)