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

@app.route("/restaurants/<res_name>", methods=["PUT", "DELETE"])
def update_restaurant(res_name):
    if request.method=="PUT":
        body=request.get_json()
        res = {
            "name": res_name,
            "address": body["address"]
        }

        for temp_res in restaurant_list:
            if temp_res["name"] == res_name:
                temp_res.update(res)
                return res_name + " updated, success!"
        return res_name + " restaurant not found!"
    else:
        for temp_res in restaurant_list:
            if temp_res["name"] == res_name:
                restaurant_list.remove(temp_res)
                return "Successfully deleted " + res_name
        return "Unable to delete " + res_name
    


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

@app.route("/restaurants/<res_name>/items/<item_name>", methods=["PUT", "DELETE"])
def update_menu_item(res_name, item_name):
    if request.method == "PUT":
        body = request.get_json()
        item ={
            "item_description": body['item_description'],
            "item_price": body['item_price']
        }

        if res_name not in menu_items:
            return "error: restaurant " + res_name + "does not exist"

        for temp_item in menu_items[res_name]:
            if temp_item['item_name'] == item_name:
                temp_item.update(item)
                return "Success, updated restaurant menu " + item_name
        return "Cannot find item " + item_name + " in restaurant " + res_name
    else:
        if res_name not in menu_items:
            return "error: restaurant " + res_name + "does not exist"
        
        for temp_item in menu_items[res_name]:
            if temp_item['item_name'] == item_name:
                menu_items[res_name].remove(temp_item)
                return "Successfully deleted " + item_name
        return "Unable to delete item"

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
        if limit is None:
            limit = 500000000000
        return json.dumps(reviews[res_name][:int(limit)])

#Week 5
#Homework Starts Here

@app.route("/restaurants/<res_name>/reviews/<review_username>", methods=["PUT", "DELETE"])
def update_reviews(res_name, review_username):
    if request.method == "PUT":
        body = request.get_json()
        item ={
            "review_stars": body['review_stars'],
            "review_comment": body['review_comment']
        }

        if res_name not in reviews:
            return "error: restaurant " + res_name + "does not exist"

        for temp_rev in reviews[res_name]:
            if temp_rev['review_username'] == review_username:
                print(temp_rev['review_username'])
                temp_rev.update(item)
                return "Success, updated restaurant review from " + review_username
        return "Cannot find " + review_username + "s review in restaurant " + res_name
    else:
        if res_name not in reviews:
            return "error: restaurant " + res_name + "does not exist"
        
        for temp_rev in reviews[res_name]:
            if temp_rev['review_username'] == review_username:
                reviews[res_name].remove(temp_rev)
                return "Successfully deleted review from " + review_username
        return "Unable to delete item"



