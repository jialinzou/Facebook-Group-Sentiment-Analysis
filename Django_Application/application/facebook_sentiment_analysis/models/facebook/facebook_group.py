from django.db import models

class FacebookGroup(models.Model):
    # Usage:
    #   FacebookGroup Model, this is used to store the information regarding a facebook group
    # Columns:
    #   id          (CharField)  : Stores the unique ID for a facebook group

    id = models.CharField(max_length=100, primary_key=True)

    def __unicode__(self):
        return self.id