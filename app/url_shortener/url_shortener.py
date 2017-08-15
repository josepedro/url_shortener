from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from contextlib import closing
from marshmallow_jsonschema import JSONSchema
from flask import jsonify
from flask import json
from sqlalchemy.orm import relationship

app = Flask("url_shortener")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#sqlalchemy_utils.functions.drop_database('sqlite:////tmp/test.db')
#sqlalchemy_utils.functions.create_database('sqlite:////tmp/test.db')

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
db.drop_all()
db.create_all()

# Declare Models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(255), primary_key=True)
    #url = relationship("Url")
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

@app.route("/")
def hello_world():
    return "<strong> hello_world!!!</strong>", 200

@app.route('/users', methods=['POST'])
def create_user():
    content = request.json
    user = User(id=content['id'])
    list_users = User.query.filter(User.id.endswith(user.id)).all()
    if list_users == []:
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
    	return jsonify(user_schema.dump(user).data), 201, {'Content-Type': 'application/json'}
    else:
        return request.data, 409, {'Content-Type': 'application/json'} 

@app.route('/user/<id>')
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
    url = Url(url=content['url'], shortUrl='testtestShort')
    user.urls.append(url)
    db.session.add(url)
    db.session.add(user)
    db.session.commit()
    url_schema = UrlSchema()
    return jsonify(url_schema.dump(url).data), 201, {'Content-Type': 'application/json'}

def main():
	app.run(host='0.0.0.0', port=8000)
