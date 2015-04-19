from .models import *
from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext

def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

def user_profile(request, user_id=None):
    return render_to_response("profile.html", context_instance=RequestContext(request))


def edit_profile(request, user_id=None):
    return render_to_response("editProfile.html", context_instance=RequestContext(request))
