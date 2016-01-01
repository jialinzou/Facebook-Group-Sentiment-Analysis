import json
import unittest
import urlparse
import us
from library.custom_exceptions.data_extraction_error import DataExtractionError
from library.data_extraction.yelp_data_extractor.yelp_extractor import YelpExtractor
from library.data_extraction.yelp_data_extractor.yelp_extractor_settings import num_businesses

# tests_yelp_extractor.py contains tests for testing our yelp extractor

class TestYelpExtractor(unittest.TestCase):
    #   Usage:
    #       Tests for the yelp extractor

    def setUp(self, yelp_extractor=YelpExtractor()):
        # Usage:
        #       Constructor for TestYelpExtractor. Used for setting the yelp extractor
        # Arguments:
        #       yelp_extractor (object) : an object of our YelpExtractor class

        self.yelp_extractor = yelp_extractor

    def test_01_search_urls(self):
        # Usage:
        #       Fetches urls from YelpExtractor class, and determine if the response is a URL,
        #       and there should be 50 URLS
        # Arguments:
        #       None

        # Get search URLS
        urls = self.yelp_extractor.get_search_urls(self.yelp_extractor)

        # Assert that the number of URLS should be the number of states
        self.assertEquals(len(urls), len(us.states.STATES))

        # Parse the first HTTP request
        url = urlparse.urlparse(urls[0])

        # Assert that the URL should have a scheme of HTTP
        self.assertEqual(url.scheme, "https")

    def test_02_search_info(self):
        # Usage:
        #       Uses the urls from get_search_urls function, and get their businesses info
        #       by the tornado HTTP client, then checking if the response code is 200,
        #       and the number of responses should equal to the number of urls
        # Arguments:
        #       None

        # Get a new set of urls
        urls = self.yelp_extractor.get_search_urls(self.yelp_extractor)

        # Get the business info from each url
        responses = self.yelp_extractor.get_search_info(self.yelp_extractor, urls)

        # The first response code should be 200
        self.assertEqual(responses[0].result().code, 200)

        # The amount of responses should equal to the urls
        self.assertEqual(len(responses), len(urls))

        # Convert the responses to a list of HTTP responses from futures
        responses = map(lambda x : x.result(), responses)

        # Get the list of business info from responses, and in their responses, loop through their
        # businesses, and add all of their business ID's to form a single list
        list_of_business_id = [business["id"] for response in responses for business in json.loads(response.body)["businesses"] ]

        # The amount of business ID's should be less than number of states * num of businesses to get
        self.assertLessEqual(len(list_of_business_id), len(us.states.STATES)*num_businesses)

    def test_03_business_ids(self):
        # Usage:
        #       Uses the urls from get_search_urls function, and convert the list of
        #       futures returned by the function to a list of business IDs
        # Arguments:
        #       None

        # Get a new set of urls
        urls = self.yelp_extractor.get_search_urls(self.yelp_extractor, num_business=10, states_to_retrieve=2)

        # Get the business info from each url
        responses = self.yelp_extractor.get_search_info(self.yelp_extractor, urls)

        # Convert the list of futures to a list of strings (business ID's)
        list_of_business_id = self.yelp_extractor.get_business_ids(self.yelp_extractor, responses)

        # Assert the type of list_business_id is a list
        self.assertIn("list", str(type(list_of_business_id)))

        # Assert the type of the first variable in list_business_id is a string
        self.assertIn("unicode", str(type(list_of_business_id[0])))

    def test_04_business_urls(self):
        # Usage:
        #       Fetches business URLs, and need to sign URLs to different IDs with
        #       base business API string
        # Arguments:
        #       None

        # Get a new set of urls
        urls = self.yelp_extractor.get_search_urls(self.yelp_extractor, num_business=10, states_to_retrieve=2)

        # Get the business info from each url
        responses = self.yelp_extractor.get_search_info(self.yelp_extractor, urls)

        # Convert the list of futures to a list of strings (business ID's)
        list_of_business_id = self.yelp_extractor.get_business_ids(self.yelp_extractor, responses)

        # Get signed URLs of each business ID
        signed_business_urls = self.yelp_extractor.get_business_urls(self.yelp_extractor, list_of_business_id)

        # Parse the first HTTP request
        url = urlparse.urlparse(signed_business_urls[0])

        # Assert that the URL should have a scheme of HTTP
        self.assertEqual(url.scheme, "https")

    def test_05_business_info(self):
        # Usage:
        #       Uses the urls from get_business_urls function, and get their businesses info
        #       by the tornado HTTP client, then checking if the response code is 200,
        #       and the number of responses should equal to the number of urls
        # Arguments:
        #       None

        # Get a new set of urls
        urls = self.yelp_extractor.get_search_urls(self.yelp_extractor)

        # Get the business info from each url
        responses = self.yelp_extractor.get_search_info(self.yelp_extractor, urls)

        # Convert the list of futures to a list of strings (business ID's)
        list_of_business_id = self.yelp_extractor.get_business_ids(self.yelp_extractor, responses)

        # Get signed URLs of each business ID
        signed_business_urls = self.yelp_extractor.get_business_urls(self.yelp_extractor, list_of_business_id)

        # Get the business info from each url
        responses = self.yelp_extractor.get_business_info(self.yelp_extractor, signed_business_urls)

        # The first response code should be 200
        self.assertEqual(responses[0].result().code, 200)

        # The amount of businesses should be less than number of states * num of businesses to get
        self.assertLessEqual(len(responses), len(us.states.STATES)*num_businesses)

    def test_06_business_urls(self):
        # Usage:
        #       Uses the urls from get_business_urls function, and convert the list of
        #       futures returned by the function to a list of business IDs
        # Arguments:
        #       None

        # Get a new set of urls
        urls = self.yelp_extractor.get_search_urls(self.yelp_extractor, num_business=10, states_to_retrieve=2)

        # Get the business info from each url
        responses = self.yelp_extractor.get_search_info(self.yelp_extractor, urls)

        # Convert the list of futures to a list of strings (business ID's)
        list_of_business_id = self.yelp_extractor.get_business_ids(self.yelp_extractor, responses)

        # Get signed URLs of each business ID
        signed_business_urls = self.yelp_extractor.get_business_urls(self.yelp_extractor, list_of_business_id)

        # Get a list of responses in each signed_business_urls
        responses = self.yelp_extractor.get_business_info(self.yelp_extractor, signed_business_urls)

        # Get business urls from each url
        business_urls = self.yelp_extractor.get_business_info_urls(self.yelp_extractor, responses)

        # Assert the type of list_business_id is a list
        self.assertIn("list", str(type(business_urls)))

        # Assert the type of the first item's url in list_business_id is a string
        self.assertIn("unicode", str(type(business_urls[0]["url"])))

        # Assert the type of the first item's review_count in list_business_id is a int
        self.assertIn("int", str(type(business_urls[0]["review_pages"])))

    def test_07_business_reviews(self):
        # Usage:
        #       Uses the urls from get_business_urls function, and convert the list of
        #       futures returned by the function to a list of business IDs. Then we use
        #       the urls to get the ID + review text + star.
        # Arguments:
        #       None

        # Get a new set of urls
        urls = self.yelp_extractor.get_search_urls(self.yelp_extractor, num_business=1, states_to_retrieve=1)

        # Get the business info from each url
        responses = self.yelp_extractor.get_search_info(self.yelp_extractor, urls)

        # Convert the list of futures to a list of strings (business ID's)
        list_of_business_id = self.yelp_extractor.get_business_ids(self.yelp_extractor, responses)

        # Get signed URLs of each business ID
        signed_business_urls = self.yelp_extractor.get_business_urls(self.yelp_extractor, list_of_business_id)

        # Get a list of responses in each signed_business_urls
        responses = self.yelp_extractor.get_business_info(self.yelp_extractor, signed_business_urls)

        # Get business urls from each url
        business_urls = self.yelp_extractor.get_business_info_urls(self.yelp_extractor, responses)

        # Get all the data from parsing the webpage
        review_data = self.yelp_extractor.get_reviews_info(self.yelp_extractor, business_urls)

        # Assert that the first item should be a dictionary
        self.assertIn("dict", str(type(review_data[0])))

        # Assert that review should be a string
        self.assertIn("unicode", str(type(review_data[0]["review"])))

        # Assert that ID should be string
        self.assertIn("unicode", str(type(review_data[0]["id"])))

        # Assert that star should a float
        self.assertIn("float", str(type(review_data[0]["star"])))

    def test_08_celery_extraction(self):
        # Usage:
        #       Uses the distributed_find_reviews to test if we can get
        #       results through celery
        # Arguments:
        #       None

        # The number of results that we want
        results_required = 10

        # Temporary store the results
        results_store = []

        # We want 10 results, and if we have 1 parallel API, then it means that we will
        # get parallel_api * random_states * business_per_state results, which is
        # 1 * 2 * 5 = 10 results
        for result in self.yelp_extractor.distributed_find_reviews(reviews_required=results_required, offset_max=0,
                                                                   random_states=1, business_per_state=1, parallel_search_api=1):

            # Store the results
            results_store.append(result["data"])

            # Should have no exceptions
            self.assertFalse(isinstance(result["exception"], DataExtractionError))

            # Results should not be None
            self.assertNotEqual(result["data"], None)

            # Assert that review should be a string
            self.assertIn("unicode", str(type(result["data"]["review"])))

            # Assert that ID should be string
            self.assertIn("unicode", str(type(result["data"]["id"])))

            # Assert that start should be a float
            self.assertIn("float", str(type(result["data"]["star"])))

            print result["data"]

        # Assert that we have 10 items
        self.assertTrue(len(results_store) == results_required)

        # Assert that we have no None inside our results_store array
        self.assertTrue(None not in results_store)