from flask import Flask, request, render_template, jsonify
import pymongo
from pymongo import MongoClient
import json
import dns
from bson import json_util
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

cluster = MongoClient("mongodb+srv://shahed:shaheddb@cluster0.dpjxz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = cluster['School']
collection = db['students']

# collection.insert_one({"_id":1, "name":"Arun"})


@app.route('/', methods=["GET","POST"])
def hookapi():
    data = collection.find()
    res = []
    for x in data:
        doc = json.dumps(x, default=json_util.default)
        res.append(json.loads(doc))
    return {"data":res}

@app.route('/webhook', methods=["GET","POST"])
def webhooks():
    return render_template('webhook.html')

@app.route('/hooks', methods=["POST"])
def hooks():
    change = request.json
    print(change)
    collection.insert_one({"data":change})
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True)
# mongodb+srv://shahed:<shaheddb>@cluster0.dpjxz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority