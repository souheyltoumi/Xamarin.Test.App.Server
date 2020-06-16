from flask import Flask,request,jsonify,redirect
from flask_pymongo import PyMongo
import hashlib, binascii, os
import json
from flask_cors import CORS
from pymongo import MongoClient
import datetime
app=Flask(__name__)
client = MongoClient("mongodb+srv://souheyl:Passatjetta25190731@xamarin-oe6oy.mongodb.net/test?retryWrites=true&w=majority")
db = client.xamarin


CORS(app)

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

@app.route('/viewposts', methods=['GET']) 
def get_bucketList():
	bucketList = db['posts']
	posts = []
	goal = bucketList.find()
	for j in goal:
		j.pop('_id')
		posts.append(j)
	return jsonify(posts)	


@app.route("/register", methods=['POST'])  
def register ():  
    bucketList = db.users
    data=request.get_json()
    username=data['username'] 
    password1=hash_password( data['password'])
    user=bucketList.find({"username":username})
    if(user.count()==0):
        bucketList.insert({ "username":username, "password":password1})
        return 'User Created 200OK'
    else:
        return 'User Already Exist 403' 

@app.route("/addpost", methods=['POST'])  
def addpost ():  
    bucketList = db.posts
    
    data=request.get_json()
    username=data['username'] 
    description=data['description'] 
    date= datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

    if(username!="" and description!="" and date!=""):
        bucketList.insert({ "username":username, "description":description,"date":date})
        return 'Post Created 200OK' 
    else:
        return 'Post  Error 403' 


@app.route("/login", methods=['POST'])  
def login ():  
    bucketList = db.users
    data=request.get_json()
    username=data['username'] 
    password=data['password'] 

    user=bucketList.find({"username":username})
    if user.count() ==0:
        return "not found"
    else:
        users=[]
        for j in user:
            j.pop('_id')
            if (verify_password( j['password'],password)):
                users.append(j)
                return jsonify(users)
            else:
                return "Wrong Password"
                
if __name__ =='__main__':
    app.run(debug=True)
