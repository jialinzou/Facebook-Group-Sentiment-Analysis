import yelp_extractor_settings
import yelp_extractor_api
from oauth2_authentication.oauth2_yelp.oauth2_yelp_authenticator import Oauth2YelpAuthenticator
from tornado_http_client.http_client import HTTPClient

# yelp_extractor.py contains the yelp_extractor class to get reviews and businesses on yelp

class YelpExtractor(object):
    # Usage:
    #       This class is responsible for using oauth2 to send yelp API requests
    #       to yelp URL endpoints.

    def __init__(self,
                 states = yelp_extractor_settings.states_of_us,
                 oauth2 = Oauth2YelpAuthenticator(),
                 http_client = HTTPClient(),
                 search_api = yelp_extractor_api.search,
                 business_api = yelp_extractor_api.business):
        # Usage:
        #       constructor for YelpExtractor, used for setting the oauth2 class,
        #       http client, and an array of states
        # Arguments:
        #       states       (array of strings) : an array of strings containing all US states
        #       oauth2       (object)           : an oauth2 object responsible for signing url requests
        #       http_client  (object)           : an http client object
        #       search_api   (string)           : an url for the search api
        #       business_api (string)           : an url fro the business api
        # Return:
        #       None

        # Set states, oauth2 class, and http client
        self.states = states
        self.oauth2 = oauth2
        self.http_client = http_client

        # Set the yelp APIs
        self.search_api = search_api
        self.business_api = business_api

    def get_search_urls(self, num_business = yelp_extractor_settings.num_businesses):
        # Usage:
        #       This function is used to get search URLS from 50 states
        # Arguments:
        #       num_business (int) : the limit on how much businesses we want to get
        # Return:
        #       None

        # For each state in urls, sign the url with the search API, and the parameters should have
        # a location (required), and the limit on how much businesses we want to get
        return [self.oauth2.sign_url(self.search_api, "GET", dict(location=location, limit=num_business)) for location in self.states]

    def get_business_info(self, urls):

        # Use http://www.google.com url to test the http client
        responses = self.http_client.get_url_requests(urls)

        # Start the ioloop
        self.http_client.start_ioloop()

        return responses