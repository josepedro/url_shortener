import os
import unittest
import tempfile
import sys
import app.url_shortener.url_shortener
from app.url_shortener.url_shortener import User
from app.url_shortener.url_shortener import UserSchema
from app.url_shortener.url_shortener import Url
from app.url_shortener.url_shortener import UrlSchema
from flask import json
from flask_sqlalchemy import SQLAlchemy
import re

class UrlShortnerTestCase(unittest.TestCase):

    def setUp(self):
        app.url_shortener.url_shortener.app.testing = True
        self.app = app.url_shortener.url_shortener.app.test_client()
        db = SQLAlchemy(app.url_shortener.url_shortener.app)
        db.drop_all()
        db.create_all()

    def tearDown(self):
    	pass
    # ------------------------------------------------------------------

    # POST /users
    def test_create_user(self):
    	db = SQLAlchemy(app.url_shortener.url_shortener.app)
        num_rows_deleted = db.session.query(User).delete()
    	db.session.commit()
    	response = self.app.post('/users', 
                       data=json.dumps(dict(id='userTest')),
                       content_type='application/json')
    	json_response = json.loads(response.data)
        assert response.status_code == 201, "Problem with code response"
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
        json_response = json.loads(response.data)
    	assert response.status_code == 409, "Problem with code conflict"
        assert json_response['id'] == 'userTest', "Problem with json response"  
    # ------------------------------------------------------------------

    # DELETE /user/:userid
    def test_delete_user(self):
    	db = SQLAlchemy(app.url_shortener.url_shortener.app)
        num_rows_deleted = db.session.query(User).delete()
        user = User(id='userTest')
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        user_schema.dump(user).data
    	response = self.app.delete('/user/userTest',
                       content_type='application/json')
    	assert response.status_code == 204, "Problem with deleting user"

    def test_delete_user_not_exist(self):
    	db = SQLAlchemy(app.url_shortener.url_shortener.app)
        num_rows_deleted = db.session.query(User).delete()
        db.session.commit()
        response = self.app.delete('/user/usasdt',
                       content_type='application/json')
    	assert response.status_code == 404, "Problem with deleting user null"    	
    # ------------------------------------------------------------------

    # POST /users/:userid/urls
    def test_create_url(self):
    	db = SQLAlchemy(app.url_shortener.url_shortener.app)
        num_rows_deleted = db.session.query(User).delete()
        user = User(id='userTest')
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        user_schema.dump(user).data
    	response = self.app.post('/users/userTest/urls', 
                       data=json.dumps(dict(url='http://www.chaordic.com.br/folks')),
                       content_type='application/json')
        json_response = json.loads(response.data)
        assert json_response['url'] == 'http://www.chaordic.com.br/folks', "Problem with url" 
        assert bool(re.search(r'[\w-]+$', json_response['shortUrl'])) == True, "Problem with short url"
    	assert response.status_code == 201, "Problem with status code"  
    # ------------------------------------------------------------------

    # GET /stats/:id
    def test_stats_url(self):
        db = SQLAlchemy(app.url_shortener.url_shortener.app)
        num_rows_deleted_user = db.session.query(User).delete()
        num_rows_deleted_url = db.session.query(Url).delete()
        user = User(id='userTest2')
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        user_schema.dump(user).data
        url = Url(url='http://www.chaordic.com.br/folks',
            shortUrl='generate_short_url(host, port)')
        user.urls.append(url)
        db.session.add(url)
        db.session.add(user)
        db.session.commit()
        url_schema = UrlSchema()
        url_schema.dump(url).data
        response = self.app.get('/stats/1', content_type='application/json')
        json_response = json.loads(response.data)
        assert json_response['id'] == 1, "Problem with id"
        assert json_response['url'] == 'http://www.chaordic.com.br/folks', "Problem with url"
        assert json_response['shortUrl'] == 'generate_short_url(host, port)', "Problem with short url"
        assert json_response['hits'] == 0, "Problem with hits"
        assert response.status_code == 200, "Problem with status code"
    # ------------------------------------------------------------------

    # GET /urls/:id
    def test_get_url(self):
        db = SQLAlchemy(app.url_shortener.url_shortener.app)
        num_rows_deleted_user = db.session.query(User).delete()
        num_rows_deleted_url = db.session.query(Url).delete()
        user = User(id='userTest2')
        db.session.add(user)
        db.session.commit()
        user_schema = UserSchema()
        user_schema.dump(user).data
        url = Url(url='http://www.chaordic.com.br/folks',
            shortUrl='generate_short_url(host, port)')
        user.urls.append(url)
        db.session.add(url)
        db.session.add(user)
        db.session.commit()
        url_schema = UrlSchema()
        url_schema.dump(url).data
        response = self.app.get('/urls/1')

        assert response.status_code == 301, "Problem with status code"
    # ------------------------------------------------------------------

    # DELETE /urls/:id
    #def test_delete_url(self):



if __name__ == '__main__':
	unittest.main()