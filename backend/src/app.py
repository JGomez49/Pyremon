
# & "c:/Users/john_/Documents/John Gonzalez/WebDevelopment/Python_React_MongoDB2/backend/venv/Scripts/Activate.ps1"

# from dotenv import load_dotenv
# load_dotenv()

import os

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)

CONNECTION_STRING = "mongodb+srv://MetaUSER:NuDmqT4Wl3JJKzen@cluster0.g7lcu.mongodb.net/MetaDB?retryWrites=true&w=majority"
# CONNECTION_STRING = os.getenv('MONGO_URI')

app.config['MONGO_URI']=CONNECTION_STRING
# app.config['MONGO_URI'] = MONGOURI

mongo = PyMongo(app)

# Esto es para que se comunique con el servidor que se va a crear
CORS(app)

db = mongo.db.usersPyFlask


@app.route('/users', methods=['POST'])
def createUser():
    #print(request.json)
    id = db.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    return jsonify(str(id.inserted_id))


@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name':doc['name'],
            'email':doc['email'],
            'password':doc['password']
        })
    return jsonify(users)


@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user = db.find_one({'_id':ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name':user['name'],
        'email':user['email'],
        'password':user['password']
    })


@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'User with id:' + id + ' deleted!'})


@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    print(request.json)
    return jsonify({'msg': 'User with id:' + id + ' updated'})



if __name__ == "__main__":
    app.run(debug=True)


