import pymongo
from flask import Flask, request, jsonify, make_response
from configparser import ConfigParser
from bson.objectid import ObjectId
import datetime
from flask_cors import CORS
import bson.json_util as json_util

app = Flask(__name__)
CORS(app)
config = ConfigParser()
config.read('app.cfg')
host = config['HOST']['host']
port = config['HOST']['port']
username = config['CREDENTIALS']['username']
password = config['CREDENTIALS']['password']

client = pymongo.MongoClient("mongodb+srv://"+username+":"+password+"@cluster0.fnvrd.mongodb.net/?retryWrites=true&w=majority")
mydb = client["Airbnb"]
house_collection = mydb["Home"]
reservation_collection = mydb["Reservation"]


@app.route('/getRandomHousesByCity')
def getRandomHousesByCity():
    house_list = []
    if request.mimetype != 'application/json':
        args = request.args
        city = args.get('city')
        count = args.get('count')
    else:
        input_json = request.get_json()
        city = input_json['city']
        count = input_json['count']
    search_list = [{"sehir": {"$regex": ".*" + city + ".*"}}]
    houses = house_collection.find({"$or": search_list}).limit(int(count))
    for i in houses:
        house_list.append(i)
    output_json = json_util.dumps(house_list, ensure_ascii=False)
    return output_json


@app.route('/getRandomHouses')
def getRandomHouses():
    house_list = []
    if request.mimetype != 'application/json':
        args = request.args
        city = args.get('city')
        count = args.get('count')
    else:
        input_json = request.get_json()
        count = input_json['count']
        city = input_json['city']
    search_list = [{"sehir": {"$not": {"$regex": ".*" + city + ".*"}}}]
    search_list1 = [{"sehir": {'$regex': '^((?!' + city + ').)*$', '$options': 'i'}}]
    houses = house_collection.find({"$or": search_list1}).limit(int(count))
    for i in houses:
        house_list.append(i)
    output_json = json_util.dumps(house_list, ensure_ascii=False)
    return output_json


if __name__ == "__main__":
    app.run(host=host, port=int(port), debug=True)