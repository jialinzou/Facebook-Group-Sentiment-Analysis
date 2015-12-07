from django.contrib import admin
from application.facebook_sentiment_analysis.models.sentiment_analysis.user_sentiment import UserSentiment

# admin_sentiment_analysis.py is used for registering sentiment_analysis models to the administrator site

admin.site.register(UserSentiment)