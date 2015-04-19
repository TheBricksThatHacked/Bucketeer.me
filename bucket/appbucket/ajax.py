from .models import *
from django.conf.urls import patterns, include, url
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

def checkoff(request):
    if (request.method != "POST"):
        return HttpResponseBadRequest("/ajax/checkoff must be accessed using POST")
    else:
        return JsonResponse({"foo": "bar"})

urlpatterns = patterns("",
    url(r'^checkoff/$', checkoff, name="checkoff"),
)