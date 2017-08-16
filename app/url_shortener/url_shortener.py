from flask import Flask
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from contextlib import closing
from marshmallow_jsonschema import JSONSchema
from flask import jsonify
from flask import json
from sqlalchemy.orm import relationship
from datetime import datetime
import string
import random

host = '0.0.0.0'
port = '8000'
app = Flask("url_shortener")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)
db.drop_all()
db.create_all()

# Declare Models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(255), primary_key=True)
    urls = db.relationship('Url', backref='user', lazy='dynamic')

class Url(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True)
    hits = db.Column(db.Integer, default=0)
    url = db.Column(db.String(255))
    shortUrl = db.Column(db.String(255))
    user_id = db.Column(db.String(255), db.ForeignKey('user.id'))

# --------------------------------------------------

# Generate Schemas from Models
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class UrlSchema(ma.ModelSchema):
    class Meta:
        model = Url

# --------------------------------------------------

# Utils functions
def generate_short_url(host, port):
    first_part = random.choice(string.letters) + random.choice(string.letters)
    last_part = str(
    (datetime.now().year) + 
    (datetime.now().month) + 
    (datetime.now().day) + 
    (datetime.now().hour) + 
    (datetime.now().minute) + 
    (datetime.now().second))
    return 'http://' + host + ':' + port + '/' + first_part + last_part 

# --------------------------------------------------

@app.route("/")
def hello_world():
    return "<strong> hello_world!!!</strong>", 200

@app.route('/users', methods=['POST'])
def create_user():
    content = request.json
    if content == None:
        return "", 404
    user = User(id=content['id'])
    list_users = User.query.filter(User.id.endswith(user.id)).all()
    if list_users == []:
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
    	return jsonify(user_schema.dump(user).data), 201, {'Content-Type': 'application/json'}
    else:
        return request.data, 409, {'Content-Type': 'application/json'} 

@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    list_users = User.query.filter(User.id.endswith(id)).all()
    if list_users == []:
        return "", 404, {'Content-Type': 'application/json'}
    else:
        User.query.filter_by(id=id).delete()
        return "", 204, {'Content-Type': 'application/json'}

@app.route('/users/<userid>/urls', methods=['POST'])
def create_url(userid):
    content = request.json
    user = User.query.filter_by(id=userid).first()
    if user == None:
        return "", 404
    url = Url(url=content['url'], shortUrl=generate_short_url(host, port))
    user.urls.append(url)
    db.session.add(url)
    db.session.add(user)
    db.session.commit()
    url_schema = UrlSchema()
    url_schema.dump(url).data
    data = json.dumps(dict(id=url.id, hits=url.hits, url=url.url, shortUrl=url.shortUrl))
    return data, 201, {'Content-Type': 'application/json'}

@app.route('/stats/<id>', methods=['GET'])
def stats_url(id):
    url = Url.query.filter_by(id=id).first()
    if url == None:
        return "", 404
    data = json.dumps(dict(id=url.id, hits=url.hits, url=url.url, shortUrl=url.shortUrl))
    return data, 200, {'Content-Type': 'application/json'}    

@app.route('/urls/<id>', methods=['GET'])
def get_url(id):
    url = Url.query.filter_by(id=id).first()
    if url == None:
        return "", 404
    url.hits += 1
    db.session.commit() 
    return redirect(url.url, code=301)

@app.route('/urls/<id>', methods=['DELETE'])
def delete_url(id):
    list_urls = Url.query.filter(Url.id.endswith(id)).all()
    if list_urls == []:
        return "", 404, {'Content-Type': 'application/json'}
    else:
        Url.query.filter_by(id=id).delete()
        return "", 204, {'Content-Type': 'application/json'}

@app.route('/users/<userId>/stats', methods=['GET'])
def stats_user(userId):
    user = User.query.filter_by(id=userId).first()
    if user == None:
        return "", 404
    urls_sorted = sorted(user.urls, key=lambda x: x.hits, reverse=True)
    if urls_sorted == []:
        urls_sorted == user.urls
    hits = sum(url.hits for url in user.urls)
    urlCount = len(urls_sorted)
    urls_dictionary = []
    total_top = 10
    if len(urls_sorted) < total_top:
        total_top = len(urls_sorted)
    for i in range(0,total_top):
        url = urls_sorted[i]
        url_dictionary = dict(id=url.id, hits=url.hits, 
            url=url.url, shortUrl=url.shortUrl)
        urls_dictionary.append(url_dictionary)        
    data = json.dumps(dict(hits=hits, urlCount=urlCount, topUrls=urls_dictionary))
    return data, 200, {'Content-Type': 'application/json'}

@app.route('/stats', methods=['GET'])
def stats_system():
    urls = Url.query.all()
    if urls == []:
        return "", 404
    urlCount = len(urls)
    hits = sum(url.hits for url in urls)
    urls_sorted = sorted(urls, key=lambda x: x.hits, reverse=True)
    if urls_sorted == []:
        urls_sorted == urls 
    urls_dictionary = []
    total_top = 10
    if len(urls) < total_top:
        total_top = len(urls)
    for i in range(0,total_top):
        url = urls_sorted[i]
        url_dictionary = dict(id=url.id, hits=url.hits, 
            url=url.url, shortUrl=url.shortUrl)
        urls_dictionary.append(url_dictionary)        
    data = json.dumps(dict(hits=hits, urlCount=urlCount, topUrls=urls_dictionary))
    return data, 200, {'Content-Type': 'application/json'}

def main():
	app.run(host=host, port=port)
