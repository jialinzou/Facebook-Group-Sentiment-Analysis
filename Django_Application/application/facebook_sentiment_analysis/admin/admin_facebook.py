from django.contrib import admin
from application.facebook_sentiment_analysis.models.facebook.facebook_user import FacebookUser
from application.facebook_sentiment_analysis.models.facebook.facebook_post import FacebookPost
from application.facebook_sentiment_analysis.models.facebook.facebook_group import FacebookGroup

# admin_facebook.py is used for registering facebook models to the administrator site

admin.site.register(FacebookUser)
admin.site.register(FacebookPost)
admin.site.register(FacebookGroup)