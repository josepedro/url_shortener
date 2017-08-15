from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from contextlib import closing
from marshmallow_jsonschema import JSONSchema
from flask import jsonify

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

'''def init_db():
    db.create_all()
    user_schema = UserSchema()
    db.session.commit()'''

@app.route("/")
def hello_world():
    return "<strong> hello_world!!!</strong>", 200

@app.route('/users', methods=['POST'])
def create_user():
    #print request.json['id']
    content = request.json
    user = User(id=content['id'])
    db.session.add(user)
    db.session.commit()
    user_schema = UserSchema()
    #print user_schema.dump(user).data
    #return jsonify(user_schema.dump(user).data), 201, {'Content-Type': 'application/json'}
    return jsonify(user_schema.dump(user).data), 201, {'Content-Type': 'application/json'}

def main():
	app.run(host='0.0.0.0', port=8000)
