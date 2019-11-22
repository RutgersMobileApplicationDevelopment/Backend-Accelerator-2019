from flask import request, abort
from pymongo import MongoClient
from bson import ObjectId
import hashlib
client = MongoClient('localhost', 27017)
restaurant_db = client['restaurant-db']

# hello("goodbye", world="earth")

def needs_auth(func):
    def nested(*args, **kwargs):
        try:
            authorization_header = request.headers.get("Authorization") #Basic <username>:<pass>
            user_password = authorization_header.split(" ")[1]
            user_password = user_password.split(":")
            username = user_password[0]
            password = user_password[1]
            hashed_pass = hashlib.sha256(password.encode()).hexdigest()
            restaurant_coll = restaurant_db["restaurants"]
            user = restaurant_coll.find_one({"username": username, "password": hashed_pass})
            if(user == None):
                abort(401)
                return
            else:
                kwargs["uid"] = user["_id"]
                return func(*args, **kwargs)
        except:
            abort(401)
            return
    nested.func_name = func.__name__
    return nested




























client = MongoClient('localhost', 27017)
restaurant_db = client['restaurant-db']

def needs_login(func):
    def check_credentials(*args, **kwargs):
        try:
            login_info = request.headers.get("Authorization")
            creds = login_info.split(" ")[1].split(":")
            hashed_pass = hashlib.sha256(creds[1].encode()).hexdigest()
            restaurant_coll = restaurant_db['restaurants']
            user = restaurant_coll.find_one({"username": creds[0], "password": hashed_pass})
            if user != None:
                kwargs["uid"]=user["_id"]
                return func(*args, **kwargs)
            else:
                abort(401)
                return
        except:
            abort(401)
            return
    check_credentials.func_name = func.__name__
    return check_credentials
