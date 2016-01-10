import math
from django.views.generic import View
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from library.data_extraction.yelp_data_extractor.yelp_extractor import YelpExtractor
from library.data_extraction.facebook_data_extractor.facebook_extractor import FacebookExtractor
from library.machine_learning.logistic_classifier import LogisticClassifier
from application.facebook_sentiment_analysis.models.yelp.yelp_review import YelpReview
from application.facebook_sentiment_analysis.models.facebook.facebook_group import FacebookGroup
from application.facebook_sentiment_analysis.models.facebook.facebook_user import FacebookUser
from application.facebook_sentiment_analysis.models.facebook.facebook_post import FacebookPost

# train.py contains a Train class to receive facebook group, and trains our sentiment analysis model

class Train(View):
    # Usage:
    #   This is used to train a SFrame logistic regression model. And return the data using a pusher.
    #   The URL parameters should contain num_samples, facebook group name, and pusher UUID channel
    #   We will get the group data such as members from the facebook group name, and train the
    #   logistic regression model with num_samples of data from amazon, and yelp (each half of num_samples)

    def setup_libraries(self):
        # Usage:
        #       The request object is an HTTPResponse object in Django. It is able to be used
        #       like an dictionary to get http parameters, such as ?num_samples=X&facebook_Group=Y.
        #       We will try to get num_samples, facebook_group, and pusher_uuid. Otherwise
        #       we will raise a SuspiciousOperation if it fails. Afterwards get data from the facebook
        #       group, and then train our model, then use our model to determine sentiment of users.
        # Arguments:
        #       yelp_extractor      (YelpExtractor)      : a yelp data extractor that can extract yelp data
        #       facebook_extractor  (FacebookExtractor)  : a facebook extractor that can extract facebook data
        #       logistic_classifier (LogisticRegression) : a logistic regression class that can compute sentiment of a user
        # Return:
        #       None

        # Setup our Libraries
        self.yelp_extractor = YelpExtractor()
        self.facebook_extractor = FacebookExtractor()
        self.logistic_classifier = LogisticClassifier()

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

        # Setup our libraries first
        self.setup_libraries()

        # get our url parameters
        num_samples, facebook_group = self.get_url_parameters(request)

        # use the group to create models for our facebook group
        facebook_message, facebook_count = self.get_facebook_group(facebook_group=facebook_group)

        # get our yelp reviews appended into a database, and we can get some message, and count
        yelp_message, yelp_count = self.get_yelp_reviews(num_samples=math.ceil(num_samples/2))

        # set user_sentiment to None
        user_sentiment = None

        # set status to success, and message to None
        status = "Success"
        message = None

        # Need to test whether if we got any yelp data
        if YelpReview.objects.count() > 0:

            # train, and get our data for user's sentiment
            user_sentiment = self.compute_sentiment_analysis(model_iterators=[YelpReview.objects.all().iterator()],
                                                             num_samples=num_samples,
                                                             facebook_group=facebook_group,
                                                             facebook_user_model=FacebookUser,
                                                             facebook_post_model=FacebookPost)

        else:

            # There is no reviews, hence we will set a message
            status = "Failure"
            message = "There are no reviews"

        # Return a JsonResponse to update to the front-end that the status is success
        return JsonResponse({'status':status, 'message':message, 'yelp_message':str(yelp_message), 'yelp_count':yelp_count,
                             'facebook_message':facebook_message, 'facebook_count':facebook_count,
                             'user_sentiment':user_sentiment})

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

        # try to get a few url parameters, such as num_samples, facebook_group, pusher_uuid
        try:

            # num_samples should be an integer, and facebook_group are strings
            num_samples = int(request.GET.get('num_samples'))
            facebook_group = request.GET.get('facebook_group')

            # return the tuples of the url parameters
            return num_samples, facebook_group

        except KeyError:
            # If we fail to get any of the url parameters, we will raise an exception for Invalid url parameters
            raise SuspiciousOperation('Invalid url parameters')

        except Exception as e:
            # Fails due to unknown reasons
            raise SuspiciousOperation('Unknown Error:%s' % str(e))

    def get_facebook_group(self, facebook_group):
        # Usage:
        #       This function will utilize the facebook_extractor to get the data using the
        #       facebook graph api, and append the data into the facebook model.
        # Arguments:
        #       facebook_group (string)  : name of the facebook group
        # Return:
        #       message        (string) : Message of the current status
        #       count          (int)    : Number of users extracted from yelp

        # First, get or create a facebook_group
        facebook_group_model, facebook_group_model_created = FacebookGroup.objects.get_or_create(id=facebook_group,
                                                                                                 defaults=dict(id=facebook_group))

        # Loop through the messages using the facebook_extractor
        for data in self.facebook_extractor.distribute_get_posts(group=facebook_group):
            # Get or create a facebook user, since that user might exist in other public groups as well
            facebook_user, facebook_user_created = FacebookUser.objects.get_or_create(id=data["user_id"],
                                                                                      defaults=dict(username=data["user_name"],
                                                                                                    facebook_group=facebook_group_model))

            # Update or create the user's messages
            FacebookPost.objects.update_or_create(id=data["message_id"], post=data["message_text"],
                                                  facebook_user=facebook_user, defaults=dict(id=data["message_id"],
                                                                                             post=data["message_text"],
                                                                                             facebook_user=facebook_user))

        # Return a facebook extractor status, and the number of users in the group
        return "Successfully finished", FacebookUser.objects.filter(facebook_group=facebook_group).count()

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

                    # Return the exception message, and how many count was added
                    return review["exception"], abs(YelpReview.objects.count()-yelp_reviews_before)

                # Add a new YelpReview into the database
                YelpReview(id=review["data"]["id"], review_text=review["data"]["review"], star=review["data"]["star"]).save()

        # There was enough reviews in the first place
        else:

            # Return a message saying that extraction was not required, and the new reviews added was 0
            return "No need for extraction, already have enough reviews", 0

        # Return a success message, and how many count was added
        return "Yelp extractor completed successfully", abs(YelpReview.objects.count()-yelp_reviews_before)

    def compute_sentiment_analysis(self, model_iterators, num_samples, facebook_group, facebook_user_model, facebook_post_model):
        # Usage:
        #       This function will utilize the logistic classifier class to
        #       compute sentiment analysis
        # Arguments:
        #       model_iterators     (list)   : list of model ierators
        #                                      each model should have ID, Review, and Star
        #       num_samples         (int)    : the number of samples to train. These will be
        #                                      divided amongst the model_iterators.
        #       facebook_group      (string) : facebook group number or ID
        #       facebook_user_model (model)  : facebook user model
        #       facebook_post_model (model)  : facebook post model
        # Return:
        #       array of dictionary (array) : an array with dictionary user_id, mean_predicted_sentiment

        # Add models to the logistic classifier
        self.logistic_classifier.add_models(model_iterators, num_samples)

        # Train the models with the current models
        self.logistic_classifier.train_model()

        # Add Facebook model data to the logistic classifier
        self.logistic_classifier.add_facebook_model(facebook_group, facebook_user_model, facebook_post_model)

        # Predict the sentiment for all the facebook posts
        self.logistic_classifier.predict_sentiment()

        # Average out each user's sentiment
        self.logistic_classifier.average_user_sentiment()

        return [dict(user_id=sentiment["user_id"],
                     username=sentiment["username"],
                     mean_predicted_sentiment=sentiment["mean_predicted_sentiment"])
                for sentiment in self.logistic_classifier.get_sentiment()]
