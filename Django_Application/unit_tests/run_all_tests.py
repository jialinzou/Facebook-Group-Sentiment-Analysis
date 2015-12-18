import os
import django
from unittest import TestLoader, TextTestRunner, TestSuite
from unit_tests.tests_http_client import TestHttpClient
from unit_tests.tests_yelp_extractor import TestYelpExtractor
from unit_tests.tests_facebook_extractor import TestFacebookExtractor

# Uses a testLoader to run multiple tests from different python unit tests file
if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

    django.setup()

    loader = TestLoader()

    from unit_tests.tests_view_index import TestViewIndex
    from unit_tests.tests_view_train import TestViewTrain

    suite = TestSuite((
            loader.loadTestsFromTestCase(TestHttpClient),
            loader.loadTestsFromTestCase(TestYelpExtractor),
            loader.loadTestsFromTestCase(TestFacebookExtractor),
            loader.loadTestsFromTestCase(TestViewIndex),
            loader.loadTestsFromTestCase(TestViewTrain)
        ))

    runner = TextTestRunner()
    runner.run(suite)