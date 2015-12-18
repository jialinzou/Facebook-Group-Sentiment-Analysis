import graphlab
import graphlab.aggregate

class LogisticClassifier(object):
    # Usage:
    #       This class is responsible for using graphlab, and takes in any models with a specified
    #       format and create a logistic classifier model.

    def __init__(self):
        # Usage:
        #       constructor for LogisticClassifier, used for setting an initial sframe
        # Arguments:
        #       None
        # Return:
        #       None

        # SFrame used for adding in model data (from yelp or amazon)
        self.sf = None

        # SFrame used for creating an sentiment model
        self.sentiment_model = None

        # SFrame for adding in facebook data
        self.facebook = None

    def add_models(self, model_iterators, num_samples):
        # Usage:
        #       add_models is used for adding rows into our initial sframe with the
        #       data from model iterators. Iterators are required since we can get large
        #       amount of data with low memory usage.
        # Arguments:
        #       model_iterators (list)   : list of model ierators
        #                                  each model should have ID, Review, and Star
        #       num_samples     (int)    : the number of samples to train. These will be
        #                                  divided amongst the model_iterators.
        # Return:
        #       num_rows        (int)    : how many samples were added

        # Loop through each model iterators
        for iterator in model_iterators:

            # Get each model inside an iterator
            for model in iterator:

                if not self.sf:
                    # Create a new sframe
                    self.sf = graphlab.SFrame(data={'id':[model.id], 'review':[model.review_text], 'star':[model.star]})
                else:
                    # Append the new row into sframe
                    self.sf = self.sf.append(graphlab.SFrame(data={'id':[model.id], 'review':[model.review_text], 'star':[model.star]}))

                # Stop if the number of samples required is appended into an sframe
                if self.sf.num_rows() >= num_samples/len(model_iterators):
                    break

            # Stop if the number of samples required is appended into an sframe
            if self.sf.num_rows() >= num_samples/len(model_iterators):
                break

        # Return the number of models that is used
        return self.sf.num_rows()

    def train_model(self, split=0.8, seed=0):
        # Usage:
        #       function to train a logistic regression model
        # Arguments:
        #       split (int) : percentage to split between training and testing
        #                     where 0.8 means 80% for training, and 20% for testing
        #       seed  (int) : the seed for random splitting training and testing
        #                     results
        # Return:
        #       None

        # Use word counts to count words with the text_analytics library in graphlab
        self.sf['word_count'] = graphlab.text_analytics.count_words(self.sf['review'])

        # Remove 3 star sentiments, since they are in the "middle"
        self.sf = self.sf[self.sf['star'] != 3]

        # Positive sentiment =  4 or 5 star review
        self.sf['sentiment'] = self.sf['star'] >= 4

        # Split the sframe into train data and test data
        train_data, test_data = self.sf.random_split(split, seed=seed)

        # The sentiment model is our logistic classifier
        self.sentiment_model = graphlab.logistic_classifier.create(train_data,
                                                                   target='sentiment',
                                                                   features=['word_count'],
                                                                   validation_set=test_data)

    def add_facebook_model(self, facebook_group, facebook_user_model, facebook_post_model):
        # Usage:
        #       function to add facebook's user and their post data
        # Arguments:
        #       facebook_group      (string) : facebook group number or ID
        #       facebook_user_model (model)  : facebook user model
        #       facebook_post_model (model)  : facebook post model
        # Return:
        #       num_rows            (int)   : number of posts added to the sframe

        # Find all users in the facebook group
        for user in facebook_user_model.objects.filter(facebook_group=facebook_group).iterator():

            # Find all the posts that the user owns
            for post in facebook_post_model.objects.filter(facebook_user=user).iterator():

                if not self.facebook:
                    # Create a new sframe
                    self.facebook = graphlab.SFrame(data={'user_id':[user.id], 'username':[user.username], 'review':[post.post]})
                else:
                    # Append to our facebook sframe
                    self.facebook = self.facebook.append(graphlab.SFrame(data={'user_id':[user.id], 'username':[user.username], 'review':[post.post]}))

        # Create a wordcount of the facebook sframe
        self.facebook['word_count'] = graphlab.text_analytics.count_words(self.facebook['review'])

    def predict_sentiment(self):
        # Usage:
        #       function to predict the sentiment on each facebook user's post
        # Arguments:
        #       None
        # Return:
        #       None

        # Predict the sentiment using the model
        self.facebook['predicted_sentiment'] = self.sentiment_model.predict(self.facebook, output_type='probability')

    def average_user_sentiment(self):
        # Usage:
        #       function to average out each user's sentiment
        # Arguments:
        #       None
        # Return:
        #       None

        # Use groupby and aggregation
        self.facebook = self.facebook.groupby(key_columns=['user_id', 'username'],
                                              operations={
                                                  'mean_predicted_sentiment':graphlab.aggregate.MEAN('predicted_sentiment')
                                              })

    def get_sentiment(self):
        # Usage:
        #       getter to return sentiment analysis results
        # Arguments:
        #       None
        # Return:
        #       facebook (sframe) : the facebook sframe that contains sentiment results

        return self.facebook

