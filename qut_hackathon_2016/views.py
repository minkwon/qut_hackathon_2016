from django.http import HttpResponse
import datetime
from django.shortcuts import render
import models
import json

# def hello(request):
#     now = datetime.datetime.now()
#     html = "<html><body>It is now %s.</body></html>" % now
#     return HttpResponse(html)

def home(request, args):
    data = models.get_tags_total_count_list()
    return render(request, 'index.html', {'data' : data})

def timeline(request):
    tag_names = "javascript,java,c#,php,python,c++,objective-c,swift,c,ruby-on-rails,bash,scala,r"
    data = models.get_timeline_data(tag_names)
    return render(request, 'timeline.html')