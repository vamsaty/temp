from flask import Flask, jsonify, request

import pymongo

from flask_pymongo import PyMongo

import json

from bson import json_util

import datetime

import base64


app = Flask(__name__)



app.config['MONGO_DBNAME'] = 'database'

app.config['MONGO_URI'] = "mongodb://localhost/database"

mongo = PyMongo(app)



@app.route('/api/v1/users', methods=['POST'])

def add_user():

    user = mongo.db.users

    username = request.json['username']

    password = request.json['password']

    old_user = user.find_one({'username' : username})

    response = jsonify({})

    if (old_user):

        response.status_code = 400

        return response

    if len(password)!=40:

        response.status_code = 405

        return response

    for a in password:

        if a not in "1234567890abcdef":

            response.status_code = 405

            return response

    user_id = user.insert({'username' : username, 'password' : password})

    new_user = user.find_one({'_id' : user_id})



    output = {'username' : new_user['username'], 'password' : new_user['password']}

    return jsonify({'result' : output})



@app.route('/api/v1/users/<name>', methods=['DELETE'])

def delete_user(name):

    user = mongo.db.users

    old_user = user.find_one({'username' : name})

    response = jsonify({})

    if (old_user):

        user.remove({"username":name})

        status_msg ="Deleted user "+name

        return jsonify({"result":status_msg})

    else:

        response.status_code = 400

        return response



@app.route('/api/v1/categories', methods=['GET'])

def get_categories():

    categories = mongo.db.categories

    docs_list  = list(categories.find())

    output=[]

    for i in docs_list:

        output.append({i['id']:i['name']})

    return jsonify({"categories": output})



@app.route('/api/v1/categories', methods=['POST'])

def add_category():

    categories = mongo.db.categories

    id = request.json['id']

    name = request.json['name']

    old_user = categories.find_one({'name' : name})

    response = jsonify({})

    if (old_user):

        response.status_code = 400

        return response

    uid = categories.insert({"id":id,"name":name})

    new_cat = categories.find_one({"_id":uid})

    output = {"id":new_cat['id'], "name":new_cat['name']}

    return jsonify({"new category added": output}), 201





@app.route('/api/v1/categories/<name>', methods=['DELETE'])

def delete_category(name):

    categories = mongo.db.categories

    old_user = categories.find_one({'name' : name})

    response = jsonify({})

    if (old_user):

        categories.remove({"name":name})

        status_msg ="Deleted category "+name

        return jsonify({"result":status_msg})

    else:

        response.status_code = 400

        return response



@app.route('/api/v1/acts', methods=['POST'])

def upload_acts():

    act = mongo.db.acts

    users = mongo.db.users



    id = request.json['actId']

    name = request.json['username']

    imgB64 = base64.encodestring(str.encode(request.json['imgB64']))

    caption = request.json['caption']

    cat = request.json['category']

    time = datetime.datetime.now().strftime("%d-%B-%Y:%S-%M-%I")

    #Validate actid

    a = act.find_one({'actid':id})

    response = jsonify({})

    if(a):

        response.status_code = 400

        return response

    #Validate username

    b = users.find_one({'username':name})

    if(b):

        uid = act.insert({'username':name, 'actId':id, 'imgB64':str(imgB64), 'caption':caption, 'category':cat, 'timestamp':time})

        new_act = act.find_one({"_id":uid})

        output = {"Caption":new_act['caption'], "Image":new_act['imgB64']}

        return jsonify({"result":output}), 201

    else:

        response.status_code = 400

        return response



    return jsonify({"result":"done"})



@app.route('/api/v1/acts/<id>', methods=['DELETE'])

def remove_acts(id):

    act = mongo.db.acts

    new_act = act.find({"actId":id})

    if(new_act):

        act.remove({"actId":id})

        status_msg ="Deleted act "+id

        return jsonify({"result":status_msg})

    else:

        response = jsonify({})

        response.status_code = 400

        return response

