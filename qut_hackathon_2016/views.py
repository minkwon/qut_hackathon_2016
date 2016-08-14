from django.http import HttpResponse
import datetime
from django.shortcuts import render
import models
import json

def hello(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def timeline(request, args):
    return render(request, 'index.html', {})

def home(request, args):
    data = models.get_tags_total_count_list()
    return render(request, 'index.html', {"data" : data})