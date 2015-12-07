from django.contrib import admin
from application.facebook_sentiment_analysis.models.yelp.yelp_review import YelpReview

# admin_yelp.py is used for registering yelp models to the administrator site

admin.site.register(YelpReview)