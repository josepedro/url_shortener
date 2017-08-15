from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from contextlib import closing
from marshmallow_jsonschema import JSONSchema
from flask import jsonify
from flask import json

app = Flask("url_shortener")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
db.create_all()

# Declare Models
class User(db.Model):
	id = db.Column(db.String(255), primary_key=True)

# Generate Schemas from Models
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

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

def main():
	app.run(host='0.0.0.0', port=8000)
