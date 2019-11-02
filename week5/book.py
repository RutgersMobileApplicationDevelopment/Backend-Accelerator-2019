import json
from flask import Flask, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)

book_db = client['book_db']

@app.route("/books", methods=['POST'])
def books():
    body = request.get_json()
    title = body["title"]
    book = {
        "title": title,
        "author": body["author"]
    }
    book_collection = book_db['books']
    if book_collection.find_one({'title':title}):
        return "Book already inserted"
    book_collection.insert_one(book)
    return "Book successfully inserted"