from flask import Flask, request
import json
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
restaurant_db = client['restaurant_db']

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route("/restaurants", methods=["POST", "GET"])
def restaurant():
    restaurant_coll = restaurant_db['restaurants']
    if request.method == "POST":
        body = request.get_json()
        res = {
            "name": body['name'],
            "address": body['address'],
            "menu_items": []
        }
        restaurant_coll.insert_one(res)
        return "Restaurant inserted"
    else:
        return JSONEncoder().encode(list(restaurant_coll.find()))