import unittest
import library.data_extraction.facebook_data_extractor.facebook_extractor_api as facebook_extractor_api
import library.data_extraction.facebook_data_extractor.facebook_extractor_settings as facebook_extractor_settings
from library.data_extraction.facebook_data_extractor.facebook_extractor import FacebookExtractor

# tests_facebook_extractor.py contains tests for the FacebookExtractor class

class TestFacebookExtractor(unittest.TestCase):
    # Usage:
    # 		Test for FacebookExtractor

    def setUp(self, facebook_extractor=FacebookExtractor(), group_id="nyutass",
              num_messages=20):
        # Usage:
        #       Constructor for TestFacebookExtractor
        # Arguments:
        # 		facebook_extractor (object) : an object of our FacebookExtractor class
        #       group_id           (string) : a default group ID or group name for testing
        #       num_messages       (int)    : the number of messages to get

        self.facebook_extractor = facebook_extractor

        self.group_id = group_id

        self.num_messages = num_messages

    def test_01_get_post_page(self):
        # Usage:
        #       Uses the group ID, and get a json response from a url
        # Arguments:
        #       None

        # Build the group url by using the group ID, number of messages to limit, and the access token
        url = facebook_extractor_api.group_url % (self.group_id.encode("utf8"), self.num_messages, facebook_extractor_settings.access_token)

        # Get the post by using get_post_page
        post = self.facebook_extractor.get_post_page.delay(self.facebook_extractor, url).get()

        # The post should be a dictionary type
        self.assertIn("dict", str(type(post)))

    def test_02_distribute_get_posts(self):
        # Usage:
        #       Uses the group ID, and uses the distribute_get_posts generator
        #       and constantly check if the 4 keys and values exists
        # Arguments:
        #       None

        # Uses the group_id and num_messages to generate multiple posts
        for post in self.facebook_extractor.distribute_get_posts(self.group_id, self.num_messages):

            # Each post should contain 4 keys
            self.assertEqual(len(post.keys()), 4)

            # Each post should have values for all the keys
            self.assertIsNotNone(post["user_id"])
            self.assertIsNotNone(post["user_name"])
            self.assertIsNotNone(post["message_id"])
            self.assertIsNotNone(post["message_text"])
