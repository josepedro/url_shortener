import os
from app.url_shortener import url_shortener
import unittest
import tempfile
import os

class UrlShortnerTestCase(unittest.TestCase):

    def setUp(self):
        flaskr.app.testing = True

    def tearDown(self):
        pass

if __name__ == '__main__':
    #print os.path.dirname(__file__)
    unittest.main()