from unittest import TestLoader, TextTestRunner, TestSuite
from unit_tests.tests_http_client import TestHttpClient
from unit_tests.tests_yelp_extractor import TestYelpExtractor
from unit_tests.tests_facebook_extractor import TestFacebookExtractor

# Uses a testLoader to run multiple tests from different python unit tests file
if __name__ == "__main__":
    loader = TestLoader()

    suite = TestSuite((
            loader.loadTestsFromTestCase(TestHttpClient),
            loader.loadTestsFromTestCase(TestYelpExtractor),
            loader.loadTestsFromTestCase(TestFacebookExtractor)
        ))

    runner = TextTestRunner()
    runner.run(suite)
