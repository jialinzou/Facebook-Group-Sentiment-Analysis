import tornado
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient

# http_client.py contains a tornado http_client object that can retrieve http_clients asynchronously

class HTTPClient(object):
    # Usage:
    #       This class is responsible for using a tornado async HTTP client to get url requests

    def __init__(self, http_client = AsyncHTTPClient(),
                 io_loop = tornado.ioloop.IOLoop.instance()):
        # Usage:
        #       constructor for HTTPClient, mainly used to setup the async http client
        #       and the ioloop
        # Arguments:
        #       http_client (object) : a tornado async http client class
        #       io_loop     (object) : a tornado IOLoop object
        # Return:
        #       None

        # Set the http_client
        self.http_client = http_client

        # Set our IOLoop
        self.io_loop = io_loop

    def get_url_requests(self, urls):
        # Usage:
        #       Uses a Tornado Async HTTP client to get multiple requests asynchronously
        # Arguments:
        #       urls      (array of strings) : an array of urls that we want to fetch our data with
        # Return:
        #       responses (array of strings) : an array of url request responses

        # Set the number of URLS that we currently have
        self.url_num = len(urls)

        # Initialize the current completed URL to 0
        self.url_current = 0

        # Return an array of fetched URL, and pass a callback
        return [self.http_client.fetch(url, self.increment_if_stop) for url in urls]

    def increment_if_stop(self, response):
        # Usage:
        #       Counts up incrementally everytime a fetch has succeeded
        # Arguments:
        #       response (string) : a string representation of a response
        # Return:
        #       None

        # Increment the url_current
        self.url_current += 1

        # If the url_current is equal to the number of url_num, then it means
        # we already reached the amount of fetched url number we requested.
        if self.url_current == self.url_num:
            # Stop the ioloop
            self.stop_ioloop()

    def stop_ioloop(self):
        # Usage:
        #       Stops an io_loop
        # Arguments:
        #       None
        # Return:
        #       None

        # Add a callback to the ioloop to stop the ioloop
        self.io_loop.add_callback(lambda x: x.stop(), self.io_loop)

    def start_ioloop(self):
        # Usage:
        #       starts an io_loop
        # Arguments:
        #       None
        # Return:
        #       None

        # Directly start an ioloop
        self.io_loop.start()