from flask import Flask, request, Response
import hashlib
import os
import subprocess
from dotenv import load_dotenv
from flask.json import jsonify
from bson import json_util
from bson.objectid import ObjectId
import dbconfig as db
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


load_dotenv()

salt = os.getenv('SALT').encode()

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"]
)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
cors = CORS(app, resources={r"*": {"origins": "http://localhost:4200"}})


@app.route('/restore', methods=['GET'])
@limiter.limit("1/minute")
def restore_db():
    os.system('call script/restore.bat')
    response = {
                'Message':'Successfully',
                'Action': 'Restoring database'
            }
    return response

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = db1.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')


@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    db1.delete_one({'username': username})
    response = jsonify({'message': 'User: ' + username +
                       ' was deleted successfully'})
    return response


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json['username']
    user = db1.find_one({'_id': ObjectId(id)})

    if user != None:
        if username:

            usernameold = user['username']
            db1.update_one({'_id': ObjectId(id)}, {'$set': {
                'username': username}})
            response = jsonify(
                {'message': 'User: ' + usernameold + ' was updated successfully to ' + username})
            return response
    else:
        return {'alert': 'Username do not match with any username account'}


@app.route('/users', methods=['GET'])
def get_users():
    users = db1.find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

db1 = db.db_users.users
db2 = db.db_users.administrators
db3 = db.db_users.developers
@app.route('/signup/<type>', methods=['POST'])
@limiter.exempt
def create_user(type):
    # 1 = usuarios 2 = administradors 3 = developers
    username = request.json['username']
    password = request.json['password'].encode()
    user = None
    query = {'username': username}
    if type == "1":
        user = db1.find_one(query)
    elif type == "2":
        user = db2.find_one(query)
    elif type == "3":
        user = db3.find_one(query)
    if user == None:
        if username and password:
            hashed_password = hashlib.pbkdf2_hmac(
                'sha512', password, salt, 100000).hex()
            
            data = {'username': username, 'password': hashed_password}
            id = None
            if type == "1":
                id = db1.insert_one(data)
            elif type == "2":
                id = db2.insert_one(data)
            elif type == "3":
                id = db3.insert_one(data)
            response = {
                'id': str(id),
                'username': username,
                'password': hashed_password
            }
            return response
        else:
            return not_found()
    else:
        return {'alert': 'Username is already taken, try to login or choose another one'}


@app.route('/signin/<type>', methods=['POST'])
@limiter.exempt
def login(type):
    user = None
    username = request.json['username']
    password = request.json['password'].encode()
    query = {'username': username}
    if type == "1":
        user = db1.find_one(query)
    elif type == "2":
        user = db2.find_one(query)
    elif type == "3":
        user = db3.find_one(query)
    hashed_password = hashlib.pbkdf2_hmac(
        'sha512', password, salt, 100000).hex()
    if user != None and hashed_password == user['password']:
        return {'message': 'Login Success',
                'response': 'welcome ' + username}
    else:
        return {'message': 'Login failed',
                'response': 'invalid username or pasword'}


@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found',
        'status': 404
    })
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(load_dotenv=True)
