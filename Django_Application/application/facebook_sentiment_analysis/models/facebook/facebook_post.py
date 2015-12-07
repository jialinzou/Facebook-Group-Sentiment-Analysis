from django.db import models
from facebook_user import FacebookUser

class FacebookPost(models.Model):
    # Usage:
    #   FacebookPost Model, this is used to store the information regarding facebook posts
    # Columns:
    #   id          (CharField)                    : Stores the unique ID for a post
    #   post        (TextField)                    : Stores the text of a post
    #   facebook_user (ForeignKey => FacebookUser) : A foreign key pointing to facebook_user

    id = models.CharField(max_length=100, primary_key=True)
    post = models.TextField()
    facebook_user = models.ForeignKey(FacebookUser)

    def __unicode__(self):
        return self.id