import oauth2
import oauth2_yelp_authenticator_settings as yelp_oauth2_settings

# oauth_2_yelp_authenticator.py contains code to create authentication

class Oauth2YelpAuthenticator(object):
    # Usage:
    #       This class is responsible for using consumer key and token to create authentication parameters
    #       for our yelp_data_extractor.

    def __init__(self,
                 consumer_key = yelp_oauth2_settings.CONSUMER_KEY,
                 consumer_secret = yelp_oauth2_settings.CONSUMER_SECRET,
                 token = yelp_oauth2_settings.TOKEN,
                 token_secret = yelp_oauth2_settings.TOKEN):
        # Usage:
        #       constructor for Oauth2YelpAuthenticator, there are multiple keys required
        #       which can be found at https://www.yelp.com/developers/manage_api_keys
        # Arguments:
        #       consumer_key    (string) : consumer key
        #       consumer_secret (string) : consumer secret
        #       token           (string) : token
        #       token_secret    (string) : token key
        # Return:
        #       None

        # Set our consumer key and token
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token = token
        self.token_secret = token_secret

        # Create a consumer that we can later use to create sign our oauth request
        self.consumer = oauth2.Consumer(self.consumer_key, self.consumer_secret)

        # Create a token with our token and token secret
        self.token = oauth2.Token(self.token, self.token_secret)

    def sign_url(self, url, method, parameters):
        # Usage:
        #       Signs a url using consumer key and token
        # Arguments:
        #       url        (string) : the url that we want to send our request to
        #       method     (string) : type of HTTP method
        #       parameters (string) : parameters for the HTTP request
        # Return:
        #       signed_url (string) : a signed url using consumer key and token

        # Get a request with our parameters
        oauth_request = oauth2.Request(method=method, url=url, parameters=parameters)

        # Update the request with timestamp, token, and consumer key
        oauth_request.update(
            {
                'oauth_nonce': oauth2.generate_nonce(),
                'oauth_timestamp': oauth2.generate_timestamp(),
                'oauth_token': self.token,
                'oauth_consumer_key': self.consumer_key
            }
        )

        # Sign our request with HMAC SHA1
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)

        # Return our oauth request
        return oauth_request.to_url()