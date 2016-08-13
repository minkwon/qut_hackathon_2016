from django.http import HttpResponse
import datetime
from django.shortcuts import render


def hello(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def timeline(request, args):
    return render(request, 'index.html', {})

def home(request, args):
    return HttpResponse("DEFAULT")