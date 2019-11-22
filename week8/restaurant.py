from flask import Flask, request, jsonify, abort
import json
from pymongo import MongoClient
from bson import ObjectId
from authentication import needs_auth
import hashlib

app = Flask(__name__)

client = MongoClient('localhost', 27017)
restaurant_db = client['restaurant-db']

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)\




# {
# 	"name": "tastygrill",
#   "address": "easton ave"
# }

@app.route("/restaurants", methods=["GET", "POST"])
def restaurants():
  if request.method == "GET":
    restaurant_coll = restaurant_db['restaurants']
    return JSONEncoder().encode(list(restaurant_coll.find({}, {"password":0})))
  else:
    body = request.get_json()
    hashed_pass = hashlib.sha256(body["password"].encode()).hexdigest()
    name = body['name']
    res = {
      "name": body['name'],
      "address": body['address'],
      "username": body['username'],
      "password": hashed_pass,
      "menu_items": []
    }
    restaurant_coll = restaurant_db['restaurants']
    restaurant_coll.insert_one(res)
    return "Restaurant inserted"

@app.route("/restaurants/<res_id>/items", methods=["GET", "POST"])
@needs_auth
def items(res_id, uid):
    if str(uid) != res_id:
        abort(401)
    restaurant_coll = restaurant_db['restaurants']
    if request.method == "GET":
        return JSONEncoder().encode(restaurant_coll.find_one({"_id": ObjectId(res_id)})["menu_items"])
    else:
        #if POST:  push to the restaurant by res_id and then push items passed in.
        restaurant_coll.update(
            {"_id": ObjectId(res_id)},
            {"$push":
                {"menu_items": request.get_json()["items"]}
            }
        )
        return "Item added to restaurant menu"

@app.route("/restaurants/<res_id>/reviews", methods=["GET", "POST"])
def reviews(res_id):
    review_collection = restaurant_db['reviews']
    if request.method == "GET":
        output = []
        for review in review_collection.find({"res_id": ObjectId(res_id)}):
            output.append(review)
        return JSONEncoder().encode(output)
    else:
        body = request.get_json()
        review = {
            "reviewer": body["reviewer"],
            "res_id": ObjectId(res_id),
            "review_body": body["review_body"]
        }
        review_collection.insert_one(review)
        return "Successful "
