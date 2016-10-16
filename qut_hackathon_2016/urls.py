from django.conf.urls import url
from django.contrib import admin
import qut_hackathon_2016.views as views

"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

urlpatterns = [
    # Examples:
    # url(r'^$', 'qut_hackathon_2016.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # if url(r'(^$)') bracket used, views.method takes request and argument

    url(r'^admin/', admin.site.urls),
    url(r'^timeline/$', views.timeline, name='timeline'),
    url(r'^timeline.json$', views.timeline_json),
    url(r'^home.json$', views.home_json),
    url(r'^$', views.home, name='home')
]