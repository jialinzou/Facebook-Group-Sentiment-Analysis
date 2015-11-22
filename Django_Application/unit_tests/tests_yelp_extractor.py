import unittest
import us
import urlparse
from data_extraction.yelp_data_extractor.yelp_extractor import YelpExtractor

# tests_yelp_extractor.py contains tests for testing our yelp extractor

class TestYelpExtractor(unittest.TestCase):
    #   Usage:
    #       Tests for the yelp extractor

    def setUp(self, yelp_extractor = YelpExtractor()):
        # Usage:
        #       Constructor for TestYelpExtractor. Used for setting the yelp extractor
        # Arguments:
        #       yelp_extractor (object) : an object of our YelpExtractor class

        self.yelp_extractor = yelp_extractor

    def test_01_business_urls(self):
        # Usage:
        #       Fetches urls from YelpExtractor class, and determine if the response is a URL,
        #       and there should be 50 URLS
        # Arguments:
        #       None

        # Get search URLS
        urls = self.yelp_extractor.get_search_urls()

        # Assert that the number of URLS should be the number of states
        self.assertEquals(len(urls), len(us.states.STATES))

        # Parse the first HTTP request
        url = urlparse.urlparse(urls[0])

        # Assert that the URL should have a scheme of HTTP
        self.assertEqual(url.scheme, "https")

    def test_02_search_urls(self):
        # Usage:
        #       Uses the urls from get_search_urls function, and get their businesses info
        #       by the tornado HTTP client, then checking if the response code is 200,
        #       and the number of responses should equal to the number of urls
        # Arguments:
        #       None

        # Get a new set of urls
        urls = self.yelp_extractor.get_search_urls()

        # Get the business info from each url
        responses = self.yelp_extractor.get_business_info(urls)

        # The first response code should be 200
        self.assertEqual(responses[0].result().code, 200)

        # The amount of responses should equal to the urls
        self.assertEqual(len(responses), len(urls))