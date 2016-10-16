from django.http import HttpResponse
import datetime
from django.shortcuts import render
import models
import json
from django.http import JsonResponse

# def hello(request):
#     now = datetime.datetime.now()
#     html = "<html><body>It is now %s.</body></html>" % now
#     return HttpResponse(html)

def home(request):
    return render(request, 'index.html')

def home_json(request):
    query = request.GET.get('query')
    result = models.get_home_json(query)
    return JsonResponse(result, safe=False)

def timeline(request):
    return render(request, 'timeline.html')

def timeline_json(request):
    query = request.GET.get('query')
    result = models.get_timeline_json(query)
    return JsonResponse(result, safe=False)