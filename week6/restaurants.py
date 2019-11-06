from flask import Flask, request, jsonify
import json
from pymongo import MongoClient
from bson import ObjectId

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
    return JSONEncoder().encode(list(restaurant_coll.find()))
  else:
    body = request.get_json()
    name = body['name']
    res = {
      "name": body['name'],
      "address": body['address'],
      "menu_items": []
    }
    restaurant_coll = restaurant_db['restaurants']
    restaurant_coll.insert_one(res)
    return "Restaurant inserted"


# {
#     "name": "madhu",
#     "price": 9 
# }

@app.route("/restaurants/<res_id>/items", methods=["GET", "POST"])
def menu_items(res_id):
    restaurant_coll = restaurant_db['restaurants']
    if request.method=="GET":
        return JSONEncoder().encode(restaurant_coll.find_one({"_id":ObjectId(res_id)})["menu_items"])
    else:
        body = request.get_json()
        item = {
            "name": body["name"],
            "price": body["price"]
        }

        restaurant_coll.update(
            {"_id": ObjectId(res_id)},
            {"$push":
                {"menu_items" : item}
            }
        )
        return "Item added to menu"

@app.route("/restaurants/<res_id>/reviews", methods=["GET","POST"])
def reviews(res_id):
    review_collection = restaurant_db["reviews"]
    if request.method == "GET":
        output = review_collection.find({"res_id":ObjectId(res_id)})
        return JSONEncoder().encode(list(output))
    else:
        body = request.get_json()
        stars = int(body["stars"])
        if(stars>5):
            return "Too many stars"
        

        review = {
            "reviewer" : body["reviewer"],
            "review_body": body["review_body"],
            "stars": int(body["stars"]),
            "res_id": ObjectId(res_id)
        }
        review_collection.insert_one(review)
        return "Successful"