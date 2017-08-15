import os
import unittest
import tempfile
import sys
import app.url_shortener.url_shortener
from app.url_shortener.url_shortener import User
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
                       data=json.dumps(dict(id='brasiial')),
                       content_type='application/json')
    	json_response = json.loads(response.data)
        assert json_response['id'] == 'brasiial', "Houston we've got a problem"    	


if __name__ == '__main__':
	unittest.main()