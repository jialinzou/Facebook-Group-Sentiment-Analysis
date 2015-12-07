from django.db import models
from facebook_group import FacebookGroup

class FacebookUser(models.Model):
    # Usage:
    #   YelpReview Model, this is used to store each reviews
    # Columns:
    #   id             (CharField)                   : Stores the unique ID user ID for a user
    #   username       (TextField)                   : Stores a text for the username
    #   facebook_group (ForeignKey => FacebookGroup) : A foreign key pointing to facebook_group

    id = models.CharField(max_length=100, primary_key=True)
    username = models.TextField()
    facebook_group = models.ForeignKey(FacebookGroup)

    def __unicode__(self):
        return self.id