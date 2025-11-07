from flask import request, jsonify, make_response
from pymongo import MongoClient
import jwt
from functools import wraps
import globals

client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.8")
db = client.Movies
movies = db.movieInfo
users = db.users
blacklist = globals.db.blacklist


def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        try:
            data = jwt.decode(token, globals.secret_key, algorithms="HS256")
        except:
            return make_response(jsonify({"message": "Token is invalid"}), 401)
        bl_token = blacklist.find_one({"token": token})
        if bl_token is not None:
            return make_response(jsonify({"message": "Token has been cancelled"}), 401)
        return func(*args, **kwargs)

    return jwt_required_wrapper


def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = request.headers["x-access-token"]
        data = jwt.decode(token, globals.secret_key, algorithms="HS256")
        if data["admin"]:
            return func(*args, **kwargs)
        else:
            return make_response(jsonify({"message": "Admin access required"}), 401)

    return admin_required_wrapper