# 1) write a GET route that accepts two numbers and returns their product
# 2) write a GET route that accepts a number and returns its square
# 3) write a combination of GET and POST routes that stores and returns a list of books that you have read, similar to what we did in class with test scores.
#    Understand how to put JSON in the Body of a request in Postman, and how to read the body of the request in your Flask server.

from flask import Flask
from flask import request
import json
import math
app = Flask(__name__)

# http://localhost:5000/product?num1=2&num2=3
@app.route('/product', methods=['GET'])
def product():
    num1 = request.args.get('num1')
    num2 = request.args.get('num2')
    product = int(num1) * int(num2)
    return str(product)

# http://localhost:5000/square?num=3
@app.route('/square', methods=['GET'])
def square():
    num = request.args.get('num')
    square = pow(int(num),2)
    return str(square)

# http://localhost:5000/book
#JSON Body:
# {
#     "book_name": "Little Women"
# }
list_of_books = list()
@app.route("/books", methods = ["POST", "GET"])
def books():
    if request.method == "GET":
        return ", ".join(list_of_books)
    elif request.method == "POST":
        book = request.get_json()['book_name']
        list_of_books.append(book)
        return "Added book: " + book
