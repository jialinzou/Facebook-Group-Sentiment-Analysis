from django.conf.urls import url
from views.index import Index
from views.train import Train

# urls.py is used for mapping urls to different views

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'train', Train.as_view(), name='train'),
]
