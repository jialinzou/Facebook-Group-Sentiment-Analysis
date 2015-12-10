import math
from django.views.generic import View
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from library.data_extraction.yelp_data_extractor.yelp_extractor import YelpExtractor
from application.facebook_sentiment_analysis.models.yelp.yelp_review import YelpReview

# train.py contains a Train class to receive facebook group, and trains our sentiment analysis model

class Train(View):
    # Usage:
    #   This is used to train a SFrame logistic regression model. And return the data using a pusher.
    #   The URL parameters should contain num_samples, facebook group name, and pusher UUID channel
    #   We will get the group data such as members from the facebook group name, and train the
    #   logistic regression model with num_samples of data from amazon, and yelp (each half of num_samples)

    # Variables:
    #   yelp_extractor (YelpExtractor) : a yelp data extractor that can extract yelp data
    yelp_extractor = YelpExtractor()

    def get(self, request):
        # Usage:
        #       The request object is an HTTPResponse object in Django. It is able to be used
        #       like an dictionary to get http parameters, such as ?num_samples=X&facebook_Group=Y.
        #       We will try to get num_samples, facebook_group, and pusher_uuid. Otherwise
        #       we will raise a SuspiciousOperation if it fails. Afterwards get data from the facebook
        #       group, and then train our model, then use our model to determine sentiment of users.
        # Arguments:
        #       request (object) : django request object
        # Return:
        #       Json (JsonResponse) : a Json object with status = done

        # get our url parameters
        num_samples, facebook_group, pusher_uuid = self.get_url_parameters(request)

        # get our yelp reviews appended into a database, and we can get some message, and count
        yelp_message, yelp_count = self.get_yelp_reviews(num_samples=math.ceil(num_samples/2))

        # Return a JsonResponse to update to the front-end that the status is success
        return JsonResponse({'status':'success', 'yelp_message':yelp_message, 'yelp_count':yelp_count})

    def get_url_parameters(self, request):
        # Usage:
        #       The request object is an HTTPResponse object in Django. It is able to be used
        #       like an dictionary to get http parameters, such as ?num_samples=X&facebook_Group=Y.
        #       We will try to get num_samples, facebook_group, and pusher_uuid. Otherwise
        #       we will return a HttpResponseBadRequest if it fails.
        # Arguments:
        #       request (object) : django request object
        # Return:
        #       num_samples    (int)    : number of samples to train with
        #       facebook_group (string) : facebook_group string, can be a number or a string
        #       pusher_uuid    (string) : pusher_uuid, the pusher uuid to communicate

        # try to get a few url parameters, such as num_samples, facebook_group, pusher_uuid
        try:

            # num_samples should be an integer, and facebook_group, and pusher_uuid are strings
            num_samples = int(request.GET.get('num_samples'))
            facebook_group = request.GET.get('facebook_group')
            pusher_uuid = request.GET.get('pusher_uuid')

            # return the tuples of the url parameters
            return num_samples, facebook_group, pusher_uuid

        except KeyError:
            # If we fail to get any of the url parameters, we will raise an exception for Invalid url parameters
            raise SuspiciousOperation('Invalid url parameters')

        except Exception as e:
            # Fails due to unknown reasons
            raise SuspiciousOperation('Unknown Error:%s' % str(e))

    def get_yelp_reviews(self, num_samples):
        # Usage:
        #       This function will utilize the yelp_extractor to get the data using the
        #       yelp api, and append the data into the yelp model.
        # Arguments:
        #       num_samples (int)  : number of samples to get from yelp
        # Return:
        #       message     (string) : Message of the current status
        #       count       (int)    : Number of samples extracted from yelp

        # Get how many counts there are for yelp reviews before adding
        yelp_reviews_before = YelpReview.objects.count()

        # If there are less than reviews we needed, then we will add more into the database
        if yelp_reviews_before < num_samples:

            # distributed_find_reviews is a generator that will return reviews as a dictionary format
            # of dict(data, exception)
            for review in self.yelp_extractor.distributed_find_reviews(reviews_required=num_samples-yelp_reviews_before):

                # If there is an issue raised inside the generator
                if review["exception"]:

                    # Get how many counts we added

                    # Return the exception message, and how many count was added
                    return review["exception"].message, abs(YelpReview.objects.count()-yelp_reviews_before)

                # Add a new YelpReview into the database
                YelpReview(id=review["data"]["id"], review_text=review["data"]["review"], star=review["data"]["start"]).save()

        # There was enough reviews in the first place
        else:

            # Return a message saying that extraction was not required, and the new reviews added was 0
            return "No need for extraction, already have enough reviews", 0

        # Return a success message, and how many count was added
        return "Yelp extractor completed successfully", abs(YelpReview.objects.count()-yelp_reviews_before)