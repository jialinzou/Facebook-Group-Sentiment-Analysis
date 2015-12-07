from django.shortcuts import render
from django.views.generic import View

# index.py contains the Index class to populate an index.html page for our user

class Index(View):
    def get(self, request):
        return render(request, 'index.html')