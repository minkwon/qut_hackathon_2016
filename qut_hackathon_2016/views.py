from django.shortcuts import render
from qut_hackathon_2016 import models
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


def responsiveness(request):
    return render(request, 'question.html')


def question_get(request):
    result = models.get_question_data_for_tag(request.GET)
    print(result)
    return JsonResponse(result, safe=False)


def get_tags(request):
    result = models.get_tags()
    return JsonResponse(result, safe=False)


def reliability(request):
    return render(request, 'usefulness.html')