from unittest import TestLoader, TextTestRunner, TestSuite
from unit_tests.tests_http_client import TestHttpClient

# Uses a testLoader to run multiple tests from different python unit tests file
if __name__ == "__main__":
    loader = TestLoader()

    suite = TestSuite((
            loader.loadTestsFromTestCase(TestHttpClient),
        ))

    runner = TextTestRunner()
    runner.run(suite)
