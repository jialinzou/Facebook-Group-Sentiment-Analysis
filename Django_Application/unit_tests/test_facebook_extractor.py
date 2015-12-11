import unittest
from library.data_extraction.facebook_data_extractor.facebook_extractor import FacebookExtractor

class TestFacebookExtractor(unittest.TestCase):
	# Usage:
	# 		Test for FacebookExtractor
	
	def setUp(self, facebook_extractor=FacebookExtractor()):
		# Usage:
		# 		Constructor for TestFacebookExtractor
		# Arguments:
		# 		facebook_extractor (object) : an object of our FacebookExtractor class
		self.facebook_extractor = facebook_extractor
		
	def test_01_get_message(self):
		# Usage:
		# 		Generate messages from group, and determine if messages contain 4 field
		group_id = 183117118384946
		# generate messages
		messages = self.facebook_extractor.get_message(group_id)
		message = messages.next()
		self.assertEqual(len(message), 4)
		
if __name__ == "__main__":
	unittest.main()
