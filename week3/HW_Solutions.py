import json
from flask import Flask, request
app = Flask(__name__)

restaurant_list = list()
menu_items = dict()
reviews = dict()

@app.route("/restaurants", methods=["POST", "GET"])
def restaurants():
    if request.method == "GET":
        return json.dumps(restaurant_list)
    else:
        body = request.get_json()
        name = body["name"]
        res = {
            "name": name,
            "address": body["address"]
        }
        for item in restaurant_list:
            if item["name"] == name:
                return "Error restaurant exists already"
        restaurant_list.append(res)
        menu_items[name] = []
        reviews[name] = []
        return "Success Added new restaurant"

@app.route("/restaurants/<res_name>/items", methods=["POST", "GET"])
def add_menu_item(res_name):
    if request.method == "POST":
        body = request.get_json()
        item ={
            "item_name": body['item_name'],
            "item_res_name": res_name,
            "item_description": body['item_description'],
            "item_price": body['item_price']
        }
        if res_name not in menu_items:
            return "Error restaurant does not exist"

        for temp_item in menu_items[res_name]:
            if temp_item['item_name'] == body['item_name']:
                return "Error item exists already"
        menu_items[res_name].append(item)
        return "Success new item added to menu of "+res_name
    else:
        return json.dumps(menu_items[res_name])

#HOMEOWRK STARTING FROM HERE

@app.route("/restaurants/<res_name>/reviews", methods=["POST", "GET"])
def add_review(res_name):
    if request.method == "POST":
        body = request.get_json()
        item ={
            "review_username": body['review_username'],
            "review_res_name": res_name,
            "review_stars": body['review_stars'],
            "review_comment": body['review_comment']
        }
        if res_name not in reviews:
            return "Error restaurant does not exist"

        for r in reviews[res_name]:
            if r['review_username'] == body['review_username']:
                return "Error you have already written a review."
        reviews[res_name].append(item)
        return "Success new comment has been added to review section of "+res_name
    else:
        limit = request.args.get('limit')
        return json.dumps(reviews[res_name][:limit])
