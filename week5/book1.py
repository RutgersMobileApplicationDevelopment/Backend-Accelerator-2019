import json
from flask import Flask, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

client = MongoClient('localhost', 27017)

book_db = client['book_db']

@app.route("/books", methods=['POST'])
def books():
    body = request.get_json()
    title = body['title']
    book = {
        "title": title,
        "author": body["author"]
    }
    book_collection = book_db['books']
    if book_collection.find_one({'title':title}):
        return "Book already inserted"
    book_collection.insert_one(book)
    return "Book successfully inserted"


#localhost:5000/books?title="Titlename"

@app.route("/books", methods=['GET'])
def find_books():
    title=request.args.get('title')
    book_collection = book_db['books']
    book_info = book_collection.find_one({'title':title})
    if title is None:
        print(list(book_collection.find()))
        return JSONEncoder().encode(list(book_collection.find()))
    elif book_info:
        return JSONEncoder().encode(book_info)
    else:
        return "book cannot be found"
