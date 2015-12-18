from django.test import TestCase, RequestFactory
from application.facebook_sentiment_analysis.views.index import Index

class TestViewIndex(TestCase):
    # Usage:
    # 		Test for facebook_sentiment_analysis index view

    def setUp(self):
        # Usage:
        #       Constructor for TestViewIndex
        # Arguments:
        # 		None

        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_01_get_index_page(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')

        # Get a response using the request
        response = Index.as_view()(request)

        # Make sure that the status code is 200
        self.assertEqual(response.status_code, 200)
