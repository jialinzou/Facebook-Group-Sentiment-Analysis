from django.contrib import admin
from models import YelpReview

# Register your models here.
class YelpReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'review_text', 'star')

admin.site.register(YelpReview, YelpReviewAdmin)