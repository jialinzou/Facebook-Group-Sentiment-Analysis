from django.db import models
from application.facebook_sentiment_analysis.models.facebook.facebook_user import FacebookUser

class UserSentiment(models.Model):
    # Usage:
    #   UserSentiment Model, this is used to store sentiment results for each user
    #   This should be a one to one relationship to the FacebookUser model
    # Columns:
    #   facebook_user (ForeignKey => FacebookUser)  : Stores the unique ID for a facebook group
    #   sentiment     (FloatField)                  : Stores sentiment value for the user

    facebook_user = models.ForeignKey(FacebookUser, primary_key=True)
    sentiment = models.FloatField()

    def __unicode__(self):
        return self.id