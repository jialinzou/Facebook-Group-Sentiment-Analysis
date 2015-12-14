import graphlab

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

        self.sf = graphlab.SFrame({'id':[], 'review':[], 'star':[]})

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

                # Create a new sframe
                sf_row = graphlab.SFrame({'id':model.id, 'review':model.review, 'star':model.star})

                # Append the new row into sframe
                self.sf.append(sf_row)

                # Stop if the number of samples required is appended into an sframe
                if num_samples/len(model_iterators) >= self.sf.num_rows():
                    break

            # Stop if the number of samples required is appended into an sframe
            if num_samples/len(model_iterators) >= self.sf.num_rows():
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
        self.sf = self.sf[self.sf['rating'] != 3]

        # Positive sentiment =  4 or 5 star review
        self.sf['sentiment'] = self.sf['rating'] >= 4

        # Split the sframe into train data and test data
        train_data, test_data = self.sf.random_split(split, seed=seed)

        # The sentiment model is our logistic classifier
        self.sentiment_model = graphlab.logistic_classifier.create(train_data,
                                                                   target='sentiment',
                                                                   features=['word_count'],
                                                                   validation_set=test_data)

    def convert_facebook_model_to_sframe(self, facebook_model_iterator1):
        pass
