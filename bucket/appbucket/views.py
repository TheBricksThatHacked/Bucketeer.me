from .models import *
from django.shortcuts import render_to_response

def index(request):

    items = Item.objects.all()
    return render_to_response("index.html", {
        'items': items
        })

def user_profile(request, user_id=None):
    return render_to_response("profile.html")
