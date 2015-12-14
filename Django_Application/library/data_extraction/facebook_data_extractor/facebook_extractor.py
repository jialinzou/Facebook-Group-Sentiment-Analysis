import json
import requests
import facebook_extractor_settings
import facebook_extractor_api
from celery import Celery

# facebook_extractor.py contains the facebook_extractor class to get group info from facebook

class FacebookExtractor(object):
    # Usage:
    #       This class is responsible for sending facebook API requests
    #       to facebook URL endpoints.

    # Sets up the celery object, and loads configuration from celery_configurations folder
    task_queue = Celery()
    task_queue.config_from_object('workload_distribution.celery_configurations.celery_config')

    # HTTP Clients:
    #   sync_http_client (object) : a blocking http client from requests
    # These are HTTP Clients that are used inside the YelpExtractor, and should not be passed
    # nor overridden into the constructor since they are not picklable (serialize)
    sync_http_client = requests

    def distribute_get_posts(self, group, num_messages=20):
        # Usage:
        #       This generator allows to use the group ID or name to extract group data from
        #       facebook using the group_url api in facebook_extractor_Settings
        # Arguments:
        #       group  (string) : a facebook group ID or name
        # Return:
        #       output (list)   : list of 20 messages  (User_ID, User_Name, Message_ID,Message_Text)
        #       next   (string) : the url of next 20 messages

        # Build the group url by using the group ID, number of messages to limit, and the access token
        url = facebook_extractor_api.group_url % (group.encode("utf8"), num_messages, facebook_extractor_settings.access_token)

        # Flag to determine if there's anymore next
        last = False

        # While it is not the last page
        while not last:

            # Get the facebook api response
            post = self.get_post_page.delay(self, url).get()

            # The data might not be inside ["feed"]["data"], but ["data"] if we
            # went to the next page
            data = None

            # Url might not be inside ["feed"]["data"] but ["data"] if we
            # went to the next page
            try:

                # If feed is inside json object's key
                if "feed" in post.keys():
                    # data is at ["feed"]["data"]
                    data = post["feed"]["data"]

                    # data is at ["feed"]["paging"]["next"]
                    url = post["feed"]["paging"]["next"]

                else:
                    # If feed is not in keys of feed, then there's only data
                    data = post["data"]

                    # url is at ["paging"]["next"]
                    url = post["paging"]["next"]

            except KeyError:
                # When we get an key error from data, that most likely means that we are on the
                # last page, so just skip
                last = True

            # Loop through data
            for message in data:
                try:
                    # get the user_id, user_name, message_id, message_text and yield it
                    yield dict(user_id=message["from"]["id"].encode("utf8"), user_name=message["from"]["name"].encode("utf8"),
                               message_id=message["id"].encode("utf8"), message_text=message["message"].encode("utf8"))
                except KeyError:
                    # some posts does not have a message_text, such as posts with pictures only
                    pass

    @task_queue.task(name='FacebookExtractor.get_user_posts')
    def get_post_page(self, url):
        # Usage:
        #       This functions uses requests and the facebook group api to get
        #       response from the facebook url endpoint
        # Arguments:
        #       url    (string) : facebook url api
        # Return:
        #       response (json) : json response from facebook group api

        # Get the response from the url
        response = self.sync_http_client.get(url).text

        # Return the json object
        return json.loads(response)