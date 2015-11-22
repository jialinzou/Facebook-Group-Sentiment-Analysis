import unittest
from tornado_http_client.http_client import HTTPClient

# tests_http_client.py contains tests for testing our tornado_http_client

class TestHttpClient(unittest.TestCase):
    #   Usage:
    #       Tests for the HTTP client.

    def setUp(self, http_client = HTTPClient()):
        # Usage:
        #       Constructor for TestHttpClient. Used for setting the http_client.
        # Arguments:
        #       http_client (object) : an object of our HTTPClient class

        self.http_client = http_client

    def test_01_request(self):
        # Usage:
        #       Fetches http://www.google.com, and starts the ioloop, then checks whether
        #       the response code is 200, and the number of responses should be 1
        # Arguments:
        #       None

        # Use http://www.google.com url to test the http client
        responses = self.http_client.get_url_requests(["http://www.google.com"])

        # Start the ioloop
        self.http_client.start_ioloop()

        # Get the results by calling result on each variable
        responses = map(lambda x : x.result(), responses)

        # Assert if the number of responses is equal to 1
        self.assertEquals(len(responses), 1)

        # Assert if the response code of the first response is 200
        self.assertEquals(responses[0].code, 200)