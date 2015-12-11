import json
#import math
#import random
import requests
import urllib
import urlparse
#import tornado.httpclient
import facebook_extractor_settings
#from bs4 import BeautifulSoup
#from celery import Celery
#from library.custom_exceptions.data_extraction_error import DataExtractionError
#from library.tornado_http_client.http_client import HTTPClient

# facebook_extractor.py contains the facebook_extractor class to get information on facebook

#celery_config
# put CELERY_IMPORTS
# CELERY_ROUTES
class FacebookExtractor(object):
    # Usage:
    #       This class is responsible for sending facebook API requests
    #       to facebook URL endpoints.

    # Sets up the celery object, and loads configuration from celery_configurations folder
#    task_queue = Celery()
#    task_queue.config_from_object('workload_distribution.celery_configurations.celery_config')

    # HTTP Clients:
    #   sync_http_client (object) : a blocking http client from requests
    # These are HTTP Clients that are used inside the YelpExtractor, and should not be passed
    # nor overridden into the constructor since they are not picklable (serialize)
    sync_http_client = requests

    def get_20messages(self, group):
		# Usage:
		#       This function gives you 20 post in the group
		# Arguments:
		#       group              (int)    : input a group that you want to fetch the posts
		# Return:
		#       output             (list)   : list of 20 messages  (User_ID, User_Name, Message_ID,Message_Text)
		#       next               (string) : the url of next 20 messages
		output = []
		message_num = 20
		url = facebook_extractor_settings.URL % ( group, message_num, facebook_extractor_settings.ACCESS_TOKEN)
		response = self.sync_http_client.get(url).text
		post = json.loads(response)
		#append all the information into a list
		for x in xrange(len(post["feed"]["data"])) :
			try: 
				output.append((post["feed"]["data"][x]["from"]["id"], post["feed"]["data"][x]["from"]["name"], post["feed"]["data"][x]["id"], post["feed"]["data"][x]["message"]) )
			except Exception as e:
				print str(e)
				pass
		next = post["feed"]["paging"]["next"]
		return (output, next)

'''
    def get_messages(self,
                     group):
        # Usage:
        #       This function gives
        # Arguments:
        #       group              (int)    : input a group that you want to fetch the posts
        # Return:
        #       output             (list)   : all the posts
 
        #generator version
        # loop all the messages out
        def loop_message(post):
            while (post["paging"]["next"]) :
                yield post
                responses = self.sync_http_client.get(post["paging"]["next"])
                post = json.load(response)            
 
        message_num = 20
        oprand = "feed.limit(%s){from,message}" % (message_num)
        url = "%s%s/?fields=%s&access_token=%s" % (self.facebook_api, group, operand, Access_token)
        responses = self.sync_http_client.get(url)
        post = json.load(response)                
        for post_i in loop_message(post) :
            for x in rangex(message_num) :
                output.append ( post_i["feed"]["data"][x]["from"]["id"], post_i["feed"]["data"][x]["from"]["name"], post_i["feed"]["data"][x]["id"], post_i["feed"]["data"][x]["message"] ) #(User_ID, User_Name, Message_ID,Message_Text) 
        return output
'''        
'''
#none generator version
        output = ''
        message_num = 20
        oprand = "feed.limit(%s){from,message}" % (message_num)
        url = "%s%s/?fields=%s&access_token=%s" % (self.facebook_api, group, operand, Access_token)
        responses = self.sync_http_client.get(url)
        post = json.load(response)
        while (post["paging"]["next"]) :
            for x in rangex(message_num) :
                output.append( post["feed"]["data"][x]["from"]["id"], post["feed"]["data"][x]["from"]["name"], post["feed"]["data"][x]["id"], post["feed"]["data"][x]["message"] ) #(User_ID, User_Name, Message_ID,Message_Text)
            responses = self.sync_http_client.get(post["paging"]["next"])
            post = json.load(response)
'''               