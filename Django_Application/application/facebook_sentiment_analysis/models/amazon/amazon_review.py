from django.db import models

class AmazonReview(models.Model):
    # Usage:
    #   AmazonReview Model, this is used to store each reviews
    # Columns:
    #   id          (CharField)  : Stores the unique ID for the review
    #   review_text (TextField)  : Stores the text for the review
    #   star        (FloatField) : Stores the star given by the user for the review

    id = models.CharField(max_length=100, primary_key=True)
    review_text = models.TextField()
    star = models.FloatField()

    def __unicode__(self):
        return self.id