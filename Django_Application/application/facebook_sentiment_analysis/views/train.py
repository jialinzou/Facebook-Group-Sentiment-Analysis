from django.views.generic import View
from django.http import JsonResponse

# train.py contains a Train class to receive facebook group, and trains our sentiment analysis model

class Train(View):
    def get(self, request):
        return JsonResponse({'foo':'bar'})