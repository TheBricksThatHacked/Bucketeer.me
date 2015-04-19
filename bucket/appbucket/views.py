from .models import *
from .forms import *
from datetime import datetime
from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext
import hashlib

#Actual messages the achievements display
achieveMsgs = {
	'one' : """<br>Congratulations, you've crossed one thing off of your bucket list!
	It's just a drop in the bucket though; keep going out and doing more things!<br><br><br>""",
	'all': """<br>Congratulations, you've completed every item on your bucket list!
	Don't rest on your laurels though; add some more things to your list and keep going!<br><br><br>""",
}

#Achievement class strings
achieveClassStrs = {
	'one' : "alert alert-success alert-info",
	'many' : "alert alert-success alert-dismissable",
}

#Achievement image urls. 
achieveImageUrls = {
	'one': "{% static \"bucket/bucketFull.png\" %}",
	'many': "{% static \"bucket/waterDropBucket.png\" %}",
}


def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

def user_profile(request, user_id=None):
    user = User.objects.get(id=user_id)
    enc_email = user.email.strip().lower().encode("utf-8")
    email_hash = hashlib.md5(enc_email).hexdigest()
    user_items = Item.objects.filter(user = user).order_by('-completed_date')
    items_completed = Item.objects.filter(user = user).exclude(completed_date__isnull=True)
    numTotal = len(user_items)
    if numTotal == 0:
      numTotal = 1
    percentCompleted = (len(items_completed) / numTotal ) * 100
    percentUnCompleted = 100 -percentCompleted
    return render_to_response("profile.html", {'percentUnCompleted': percentUnCompleted,'percentCompleted': percentCompleted, 'userProfile': user, 'email_hash': email_hash, 'user_items': user_items, 'items_completed': items_completed}, context_instance=RequestContext(request))

def my_profile(request):
    return user_profile(request, user_id=request.user.id)


def edit_profile(request, user_id=None):
    return render_to_response("edit_profile.html", context_instance=RequestContext(request))

# Create a bucket list item
def add_item(request):
    item_form = None
    if request.method == "POST":
        item_form = ItemForm(request.POST)
        if item_form.is_valid():
            i = item_form.save(commit=False)
            i.user = request.user
            if 'complete' in request.POST:
                i.completed_date = datetime.now()
            i.save()
        else:
            print("FORM NOT VALID EVERYONE PANIC")
    else:
        item_form = ItemForm()
    # TODO process tags
    context = {
        "item_form": item_form
    }
    return render_to_response('addItem.html', context, context_instance=RequestContext(request))
