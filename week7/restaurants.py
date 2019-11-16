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
        return json.JSONEncoder.default(self, o)
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
    if request.method == "GET":
        return JSONEncoder().encode(restaurant_coll.find_one({"_id": ObjectId(res_id)})["menu_items"])
    else:
        body = request.get_json()
        item = {
            "name": body["name"],
            "price": int(body["price"])
        }

        restaurant_coll.update(
            {"_id": ObjectId(res_id)},
            {"$push":
                 {"menu_items": item}
             }
        )
        return "Item added to menu"


@app.route("/restaurants/<res_id>/reviews", methods=["GET", "POST"])
def reviews(res_id):
    review_collection = restaurant_db["reviews"]
    if request.method == "GET":
        output = review_collection.find({"res_id": ObjectId(res_id)})
        return JSONEncoder().encode(list(output))
    else:
        body = request.get_json()

        review = {
            "reviewer": body["reviewer"],
            "review_body": body["review_body"],
            "stars": int(body["stars"]),
            "res_id": ObjectId(res_id),
            "review_votes": int(1)
        }
        if review["stars"] > 5:
            return "Too many stars"

        review_collection.insert_one(review)
        return "Successful"

# - lets say the review object will also contain another field, called votes. when a review is made, votes should start out as 1 (like reddit).
# - create two routes:
#    1) POST /restaurants/<res_id>/reviews/<review_id>/upvote: this route will increment the likes field for this review
#    2) POST /restaurants/<res_id>/reviews/<review_id>/downvote: this route will decrement the likes field for this review
# note that we've never done routes with two <parameters> in them. in this case, your methods will look like
# def upvote(res_id, review_id): and def downvote(res_id, review_id):. this is how you handle two separate parameters in the route.
# we've also never worked with review_ids but it is the same way you find using res_ids, just on a different collection.
# make sure that the GET /restaurants/<res_id>/reviews now shows the votes for each review.

@app.route("/restaurants/<res_id>/reviews/<review_id>/upvote", methods=["POST"])
def upvote(res_id, review_id):
    restaurant_coll = restaurant_db['restaurants']
    review_collection = restaurant_db["reviews"]

    review_collection.update(
        {"_id": ObjectId(review_id)},
        {
            '$inc': {'review_votes': 1}
        }
    )
    return "Successful"


@app.route("/restaurants/<res_id>/reviews/<review_id>/downvote", methods=["POST"])
def downvote(res_id, review_id):
    restaurant_coll = restaurant_db['restaurants']
    review_collection = restaurant_db["reviews"]

    review_collection.update(
        {"_id": ObjectId(review_id)},
        {
            '$inc': {'review_votes': -1}
        }
    )
    return "Successful"



@app.route("/restaurants/reviews",methods=["GET"])
def get_reviews():
    res_name = request.args.get('res_name')
    restaurant_coll = restaurant_db['restaurants']
    itm = restaurant_coll.find({"name": res_name})
    review_coll = restaurant_db['reviews']
    rest_id = []
    for item in itm:
        rest_id.append(ObjectId(item['_id']))

    docs = review_coll.find(
        {
            "res_id": {
                '$in': rest_id
            }
        }
    )

    return JSONEncoder().encode(list(docs))

