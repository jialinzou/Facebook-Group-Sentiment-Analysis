import json
from django.test import TestCase, RequestFactory
from django.core import serializers
from application.facebook_sentiment_analysis.views.train import Train

class TestViewTrain(TestCase):
    # Usage:
    # 		Test for facebook_sentiment_analysis index view

    def setUp(self):
        # Usage:
        #       Constructor for TestViewIndex
        # Arguments:
        # 		None

        # Every test needs access to the request factory.
        self.factory = RequestFactory()

        # An array of model file locations
        model_array = [
            "./unit_tests/serialized_test_data/yelp/review.json",
            "./unit_tests/serialized_test_data/facebook/group.json",
            "./unit_tests/serialized_test_data/facebook/post.json",
            "./unit_tests/serialized_test_data/facebook/user.json"
        ]

        # Loop through model file locations
        for file_locations in model_array:

            # Open the file
            with open(file_locations) as data_file:

                # Read the file
                data = data_file.read()

                # Loop through each data string, and deserializea, and save the models
                for deserialized_object in serializers.deserialize("json", data):
                    deserialized_object.save()

    def test_01_get_train_json(self):
        # Create an instance of a GET request.
        request = self.factory.get('/train?num_samples=500&facebook_group=nyutass')

        # Get a response using the request
        response = Train.as_view()(request)

        # Get json representation of response
        json_status = json.loads(response.content)

        # Make sure that the status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure that the status is success
        self.assertEqual(json_status["status"], "Success")

        # Yelp Count should be 0 since we have all the data serialized
        self.assertEqual(json_status["yelp_count"], 0)

        # Facebook Message should be successfully finished
        self.assertEqual(json_status["facebook_message"], "Successfully finished")

        # User Sentiment should be an array
        self.assertIn("list", str(type(json_status["user_sentiment"])))

        # Facebook Count should be 47
        self.assertEqual(json_status["facebook_count"], 47)

        # Yelp Message should be no need for extraction
        self.assertEqual(json_status["yelp_message"], "No need for extraction, already have enough reviews")