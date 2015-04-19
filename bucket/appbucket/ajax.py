from datetime import datetime
from .models import *
from django.conf.urls import patterns, include, url
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404

def checkoff(request):
    if (request.method != "POST"):
        return HttpResponseBadRequest("/ajax/checkoff must be accessed using POST")
    response = {
        "success": False,
        "checked": False,
    }
    item_id = request.POST["item-id"]
    item = get_object_or_404(Item, id=item_id)
    if (item.user.id != request.user.id):
        return HttpResponseForbidden("You do not have access to that item")
    # passed the gauntlet, modify things
    item.completed_date = datetime.now()
    item.save()
    response["checked"] = True
    return JsonResponse(response)

urlpatterns = patterns("",
    url(r'^checkoff/$', checkoff, name="checkoff"),
)