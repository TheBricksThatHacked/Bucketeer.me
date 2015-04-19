from .models import *
from .forms import *
from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext

def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

def user_profile(request, user_id=None):
    return render_to_response("profile.html", context_instance=RequestContext(request))

def my_profile(request):
    return user_profile(request, user_id=request.user.id)


def edit_profile(request, user_id=None):
    return render_to_response("editProfile.html", context_instance=RequestContext(request))

# Create a bucket list item
def add_item(request):
    item_form = None
    if request.method == "POST":
        item_form = ItemForm(request.POST)
        if item_form.is_valid():
            i = item_form.save(commit=False)
            i.user = request.user
            i.save()
    else:
        item_form = ItemForm()
    # TODO process tags
    context = {
        "item_form": item_form
    }
    return render_to_response('addItem.html', context, context_instance=RequestContext(request))
