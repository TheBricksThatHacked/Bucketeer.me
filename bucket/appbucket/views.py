from .models import *
from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext
import hashlib

def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

def user_profile(request, user_id=None):
    user = User.objects.get(id=user_id)
    enc_email = user.email.strip().lower().encode("utf-8")
    email_hash = hashlib.md5(enc_email).hexdigest()
    return render_to_response("profile.html", {'userProfile': user, 'email_hash': email_hash}, context_instance=RequestContext(request))

def my_profile(request):
    return user_profile(request, user_id=request.user.id)


def edit_profile(request, user_id=None):
    return render_to_response("editProfile.html", context_instance=RequestContext(request))

def add_item(request, user_id=None):
    return render_to_response("addItem.html", context_instance=RequestContext(request))
