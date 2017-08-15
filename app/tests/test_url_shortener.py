import os
import unittest
import tempfile
import sys
import app.url_shortener.url_shortener
from app.url_shortener.url_shortener import User
from app.url_shortener.url_shortener import UserSchema
from flask import json
from flask_sqlalchemy import SQLAlchemy

class UrlShortnerTestCase(unittest.TestCase):

    def setUp(self):
        app.url_shortener.url_shortener.app.testing = True
        self.app = app.url_shortener.url_shortener.app.test_client()

    def tearDown(self):
    	pass

    def test_create_user(self):
    	db = SQLAlchemy(app.url_shortener.url_shortener.app)
        num_rows_deleted = db.session.query(User).delete()
    	db.session.commit()
    	response = self.app.post('/users', 
                       data=json.dumps(dict(id='userTest')),
                       content_type='application/json')
    	json_response = json.loads(response.data)
        assert json_response['id'] == 'userTest', "Problem with json response"    	

    def test_create_user_exists(self):
        db = SQLAlchemy(app.url_shortener.url_shortener.app)
        num_rows_deleted = db.session.query(User).delete()
        user = User(id='userTest')
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        user_schema.dump(user).data
        response = self.app.post('/users', 
                       data=json.dumps(dict(id='userTest')),
                       content_type='application/json')
    	assert response.status_code == 409, "Problem with code conflict"

    def test_delete_user(self):
    	db = SQLAlchemy(app.url_shortener.url_shortener.app)
        num_rows_deleted = db.session.query(User).delete()
        user = User(id='userTest')
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        user_schema.dump(user).data
    	response = self.app.get('/user/userTest',
                       content_type='application/json')
    	assert response.status_code == 204, "Problem with deleting user"

    def test_delete_user_not_exist(self):
    	db = SQLAlchemy(app.url_shortener.url_shortener.app)
        num_rows_deleted = db.session.query(User).delete()
        db.session.commit()
        response = self.app.get('/user/usasdt',
                       content_type='application/json')
        print response.status_code
    	assert response.status_code == 404, "Problem with deleting user null"    	

if __name__ == '__main__':
	unittest.main()