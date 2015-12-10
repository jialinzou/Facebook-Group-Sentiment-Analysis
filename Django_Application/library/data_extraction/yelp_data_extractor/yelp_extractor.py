import json
import math
import random
import requests
import urllib
import urlparse
import tornado.httpclient
import yelp_extractor_api
import yelp_extractor_settings
from bs4 import BeautifulSoup
from celery import Celery
from library.custom_exceptions.data_extraction_error import DataExtractionError
from library.oauth2_authentication.oauth2_yelp.oauth2_yelp_authenticator import Oauth2YelpAuthenticator
from library.tornado_http_client.http_client import HTTPClient

# yelp_extractor.py contains the yelp_extractor class to get reviews and businesses on yelp


class YelpExtractor(object):
    # Usage:
    #       This class is responsible for using oauth2 to send yelp API requests
    #       to yelp URL endpoints, and extract yelp review data.

    # Sets up the celery object, and loads configuration from celery_configurations folder
    task_queue = Celery()
    task_queue.config_from_object('workload_distribution.celery_configurations.celery_config')

    # HTTP Clients:
    #   http_client      (object) : an async http client from tornado
    #   sync_http_client (object) : a blocking http client from requests
    # These are HTTP Clients that are used inside the YelpExtractor, and should not be passed
    # nor overridden into the constructor since they are not picklable (serialize)
    http_client = HTTPClient()
    sync_http_client = requests

    def __init__(self,
                 states=yelp_extractor_settings.states_of_us,
                 oauth2=Oauth2YelpAuthenticator(),
                 search_api=yelp_extractor_api.search,
                 business_api=yelp_extractor_api.business):
        # Usage:
        #       constructor for YelpExtractor, used for setting the oauth2 class,
        #       http client, and an array of states
        # Arguments:
        #       states           (array of strings) : an array of strings containing all US states
        #       oauth2           (object)           : an oauth2 object responsible for signing url requests
        #       search_api       (string)           : an url for the search api
        #       business_api     (string)           : an url fro the business api
        # Return:
        #       None

        # Set states, oauth2 class, tornado HTTP client, and requests http client
        self.states = states
        self.oauth2 = oauth2

        # Set the yelp APIs
        self.search_api = search_api
        self.business_api = business_api

    @task_queue.task(name='YelpExtractor.get_search_urls')
    def get_search_urls(self,
                        num_business=yelp_extractor_settings.num_businesses, offset=0,
                        states_to_retrieve=yelp_extractor_settings.num_of_states):
        # Usage:
        #       This function is used to get search URLS from states
        # Arguments:
        #       num_business       (int)    : the limit on how much businesses we want to get
        #       offset             (int)    : the offset of the search, if we set it to 20, then it
        #                                     will search from 20~20+num_business
        #       states_to_retrieve (int)    : the amount of states we want to retrieve
        # Return:
        #       urls         (list of urls) : a list of search api urls

        # For each state in urls, sign the url with the search API, and the parameters should have
        # a location (required), and the limit on how much businesses we want to get
        return [self.oauth2.sign_url(self.search_api, "GET", dict(location=location, limit=num_business, offset=offset)) for location in random.sample(self.states, states_to_retrieve)]

    @task_queue.task(name='YelpExtractor.get_search_info')
    def get_search_info(self, urls):
        # Usage:
        #       This function is used to get search's info from the URLS using
        #       our Tornado HTTP Client
        # Arguments:
        #       urls    (list of URLs)    : a list of urls that contains a state each in url's parameters
        # Return:
        #       futures (list of futures) : a list of futures containing the result of each request

        # Feed in our urls
        responses = self.http_client.get_url_requests(urls)

        # Start the ioloop
        self.http_client.start_ioloop()

        # Return the responses
        return responses

    @task_queue.task(name='YelpExtractor.get_business_ids')
    def get_business_ids(self, responses):
        # Usage:
        #       This function is used to extract all of the business ID's in a list of futures
        #       containing HTTP responses
        # Arguments:
        #       responses           (list of futures) : a list of futures containing the result of each request
        # Return:
        #       list_of_business_id (list of string)  : a flat list of IDs

        # First map the results from futures to HTTP response object
        responses = map(lambda x : x.result(), responses)

        # Get the list of business info from responses, and in their responses, loop through their
        # businesses, and add all of their business ID's to form a single list
        return [business["id"] for response in responses for business in json.loads(response.body)["businesses"]]

    @task_queue.task(name='YelpExtractor.get_business_urls')
    def get_business_urls(self, business_ids):
        # Usage:
        #       This function is used to get URLs from each business, so that
        #       we can scrape it later using beautiful soup 4
        # Arguments:
        #       business_ids (list of strings) : a list of business IDs
        # Return:
        #       urls         (list of urls)    : a list of business api urls

        # For each state in urls, sign the url with the search API, and the parameters should have
        # a location (required), and the limit on how much businesses we want to get
        return [self.oauth2.sign_url(urlparse.urljoin(self.business_api, urllib.quote(business_id.encode('utf8'))), "GET", dict()) for business_id in business_ids]

    @task_queue.task(name='YelpExtractor.get_business_info')
    def get_business_info(self, urls):
        # Usage:
        #       This function is used to businesses' info from the URLS using
        #       our Tornado HTTP Client
        # Arguments:
        #       urls    (list of URLs)    : a list of urls that contains a state each in url's parameters
        # Return:
        #       futures (list of futures) : a list of futures containing the result of each request

        # Feed in our urls
        responses = self.http_client.get_url_requests(urls)

        # Start the ioloop
        self.http_client.start_ioloop()

        # Return the responses
        return responses

    @task_queue.task(name='YelpExtractor.get_business_info_urls')
    def get_business_info_urls(self, responses):
        # Usage:
        #       This function is used to extract all of the business urls in a list of futures
        #       containing HTTP responses
        # Arguments:
        #       responses           (list of futures) : a list of futures containing the result of each request
        # Return:
        #       list_of_business_id (list of string)  : a flat list of urls

        # First map the results from futures to HTTP response object
        responses = map(lambda x : x.result(), responses)

        # Get the list of business info from responses, and in their responses, loop through their
        # businesses, and add all of their business ID's and review counts into to form a single list.
        return [dict(url=json.loads(response.body)["url"],
                     review_pages=int(math.ceil(int(json.loads(response.body)["review_count"])/20)+1)) for response in responses]

    @task_queue.task(name='YelpExtractor.get_reviews_info')
    def get_reviews_info(self, url_reviews):
        # Usage:
        #       This function will be used to get all the reviews in a page, and their respective stars
        #       and return a dictionary with id + review + stars
        # Arguments:
        #       url_reviews  (list of dict) : a list of dictionary with url and review_pages key
        # Return:
        #       reviews_info (list of dict) : a flat list of urls

        # Compute a list of reviews urls using url + review_pages
        urls = [urlparse.urljoin(url_info["url"], "?start="+str(num*20)) for url_info in url_reviews for num in xrange(url_info["review_pages"])]

        # Feed in our urls
        responses = self.http_client.get_url_requests(urls)

        # Start the ioloop
        self.http_client.start_ioloop()

        # Each responses now contain a webpage body, but we should map it back to
        # result first, then to a body
        responses = map(lambda x : x.result().body, responses)

        # We want to make a dictionary of ID, Review Text, and Stars using beautifulsoup
        reviews_info = []

        # Responses will contain multiple responses with body, we need to loop through them
        for body in responses:
            # Create a soup using the body, and a html parser
            soup = BeautifulSoup(body, 'html.parser')

            # We can get the number of reviews by counting the review_wrapper
            soup_review_with_sidebar = soup.find_all(attrs={"class": "review review--with-sidebar"})
            for count_review in xrange(len(soup_review_with_sidebar)):
                try:
                    # We can get ID by looking at the review review--with-sidebar div class
                    # with the data-review-id attribute. We then can get the review by getting the review-wrapper's
                    # p tag, and then the start with the i tag's title attribute and then splitting by space and
                    # getting the first value
                    soup_review = soup_review_with_sidebar[count_review]
                    id = soup_review["data-review-id"]
                    review = soup_review.find_all(attrs={"class": "review-wrapper"})[0].p.getText()
                    star = float(soup_review.find_all(attrs={"class": "review-wrapper"})[0].i["title"].split(" ")[0])

                    # After getting all these 3 variables, append it into a list
                    reviews_info.append(dict(id=id, review=review, star=star))
                except Exception as e:
                    # It is possible that is it a text that wants us to write a review, for this case
                    # we would not be able to find a review and star, and would create an exception
                    pass

        return reviews_info

    @task_queue.task(name='YelpExtractor.determine_review_pages')
    def determine_review_pages(self, url):
        # Usage:
        #       This function is used to determine the number of reviews (pages) in a yelp URL
        #       in logarithmic time.
        # Arguments:
        #       url       (string) : a url
        # Return:
        #       num_pages (int)    : the number of pages that exists in the review
        #                            returns None if there is an algorithmic issue

        # Current number pages
        current_iteration = 0

        # A flag to raise when we find the last page
        last_page = False

        # We want to find the number of pages that will give us a empty result review page
        while not last_page:
            # Encode a dictionary of start=exponential function
            url_with_param = urlparse.urljoin(url, '?'+urllib.urlencode(dict(start=2*current_iteration*20)))

            # Feed in our url to a blocking http client
            response = self.sync_http_client.get(url_with_param)

            # Parse the response with beautiful soup
            soup = BeautifulSoup(response.text, 'html.parser')

            # If the length of the review-wrapper is equal to zero, that means we have found the
            # last page
            if len(soup.find_all(attrs={"class": "review-wrapper"})) == 0:
                last_page = True

            # Increment the iteration
            current_iteration += 1

        # Starting from here, we have found a page that does not have a review, but we will
        # need to get the number of reviews by going down logarithmically (using binary search)
        # The first page review
        first = 0

        # The last page review
        last = 2*current_iteration

        # Flag to indicate if we have found the right page
        found = False

        # While we have not found the correct number of reviews
        while first <= last and not found:
            # Get the midpoint
            midpoint = (first+last)/2

            # Encode a dictionary of start=exponential function
            url_with_param = urlparse.urljoin(url, '?'+urllib.urlencode(dict(start=midpoint*20)))

            # Feed in our url to a blocking http client
            response = self.sync_http_client.get(url_with_param)

            # Parse the response with beautiful soup
            soup = BeautifulSoup(response.text, 'html.parser')

            # If the length of the reviews = 0, that means we have found the last page
            # else, we move the first to the midpoint, and we will search again
            if len(soup.find_all(attrs={"class": "review-wrapper"})) == 0:
                return midpoint
            else:
                first = midpoint+1

        # Return 0 if we can't find anything
        return None

    def distributed_find_reviews(self, reviews_required, random_states=5, offset_max=980,
                                 business_per_state=5, parallel_search_api=5):
        # Usage:
        #       Uses celery to find reviews in a distributed fashion. It will randomly generate
        #       search URLs on the number of random_states with offset of random with a ceiling of
        #       offset_max. And keeps incrementing the offset if the review_required was less than
        #       reviews_required.
        # Arguments:
        #       reviews_required      (int) : the number of reviews that we need to get
        #       random_states         (int) : how many states chosen randomly
        #       offset_max            (int) : an offset on the search reviews
        #       business_per_state    (int) : how many businesses per state we want to get
        #       parallel_search_api   (int) : how many parallel searches we want to make using yelp search api
        # Return:
        #       Generator - 1 reviews per yield

        # The current reviews that we have
        current_reviews = 0

        # A flag indicating that we have exhausted our API calls
        api_exhaust = False

        # A flag indicating that there might be an captcha issue
        api_captcha = False

        # A flag indicating that someone else is wrong
        unknown_error = False

        # Keep looping until we get the specified amount of reviews
        while current_reviews != reviews_required and not any((api_exhaust, api_captcha, unknown_error)):

            # It is possible that we will exhaust the yelp API
            try:
                # Depending on the parallel_search_api, we will fire off multiple search api's
                # Then we will get the results by doing a get() for asyncResults.
                # The result would be an array of list, and the list would contain a list of URLs
                # that we want to create.
                search_api = map(lambda x: x.get(), [self.get_search_urls.delay(self, num_business=business_per_state,
                                                                                offset=random.randint(0, offset_max),
                                                                                states_to_retrieve=random_states) for loop in xrange(parallel_search_api)])

                # Using the array of lists, fire off each requests in each list
                # Then we will get each results by calling get
                search_api_results = map(lambda x: x.get(), [self.get_search_info.delay(self, urls) for urls in search_api])

                # search_api_results is now a list of future, we need to get the business IDs from the results
                # then map it using .get() to get all the data.
                list_of_business_id = map(lambda x: x.get(), [self.get_business_ids.delay(self, results) for results in search_api_results])

                # Using the list of business IDs, we will generate another list of signed_business_urls
                list_of_signed_business_urls = map(lambda x: x.get(), [self.get_business_urls.delay(self, business_ids) for business_ids in list_of_business_id])

                # For each list inside the list of signed business urls, we will get each responses
                business_urls_results = map(lambda x: x.get(), [self.get_business_info.delay(self, signed_business_urls) for signed_business_urls in list_of_signed_business_urls])

                # After getting all the results, we would get the URLs of each list inside business_url_results
                list_of_business_urls = map(lambda x: x.get(), [self.get_business_info_urls.delay(self, results) for results in business_urls_results])

                # We will extract all the business reviews data for each list in list_of_business_urls
                review_data = map(lambda x: x.get(), [self.get_reviews_info.delay(self, business_urls) for business_urls in list_of_business_urls])

                # Create a flat list out of the URLs data
                review_data = reduce(lambda x,y: x+y, review_data)

                # If we got nothing from our review_data, then it means we have encountered
                # captcha, which requires us to give extra inputs before proceeding
                if not review_data:
                    # Yield the review, so that the review will be passed back
                    yield dict(data=None, exception=DataExtractionError(message=str("Captcha Error"), errors="Requires captcha input"))

                    # Set captcha to be True, and end the while loop
                    api_captcha = True

                # Loop through the flattened list of review_data
                for review in review_data:

                    # Increment current_reviews
                    current_reviews += 1

                    # Yield the review, so that the review will be passed back
                    yield dict(data=review, exception=None)

                    # If the amount of required reviews has achieved, then
                    # break from the for loop
                    if current_reviews == reviews_required:
                        break

            except tornado.httpclient.HTTPError as e:
                # Yield our data with our exception we had exhausted our yelp API requests
                yield dict(data=None, exception=DataExtractionError(message=str("HTTP Error"), errors="Code:%s, Message:%s, Response:%s" % (e.code, e.message, e.response)))

                # Flag indicating that we have exhausted our API counts
                api_exhaust = True

            except Exception as e:
                # Yield our data with our exception we had an unknown error
                yield dict(data=None, exception=DataExtractionError(message=str("Unknown Error"), errors=str(e)))

                # Flag indicating that we have exhausted our API counts
                unknown_error = True