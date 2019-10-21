from flask import Flask, request
import random
app = Flask(__name__)

@app.route("/random", methods=["GET"])
def Random():
    return str(random.randint(1, 100))

@app.route("/sum", methods=["GET"])
def Sum():
    val1 = request.args.get('val1')
    val2 = request.args.get('val2')
    val3 = int(val1) + int(val2)
    return str(val3)

testscores = []

@app.route("/testscores", methods=["POST", "GET"])
def scores():
    if request.method == "POST":
        score = request.get_json()['score']
        testscores.append(str(score))
        return "Added new score"
    else:
        return ", ".join(testscores)