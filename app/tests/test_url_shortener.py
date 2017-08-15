import os
import unittest
import tempfile
import sys
import url_shortener.url_shortener

class UrlShortnerTestCase(unittest.TestCase):

    def setUp(self):
        print "rodando a parada"
        flaskr.app.testing = True

    def tearDown(self):
        pass

    def test_first(self):
    	print "ollaa"


if __name__ == '__main__':
    #print os.path.dirname(__file__)
	unittest.main()