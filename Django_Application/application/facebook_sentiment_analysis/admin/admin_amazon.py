from django.contrib import admin
from application.facebook_sentiment_analysis.models.amazon.amazon_review import AmazonReview

# admin_amazon.py is used for registering amazon models to the administrator site

admin.site.register(AmazonReview)