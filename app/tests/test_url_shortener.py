import os
import unittest
import tempfile
import sys
import app.url_shortener.url_shortener

class UrlShortnerTestCase(unittest.TestCase):

    def setUp(self):
        app.url_shortener.url_shortener.app.testing = True

    def tearDown(self):
        pass

    def test_first(self):
    	assert 2 + 3 == 5, "Houston we've got a problem" 


if __name__ == '__main__':
	unittest.main()