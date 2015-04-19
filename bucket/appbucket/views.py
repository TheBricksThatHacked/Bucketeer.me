from .models import *
from .forms import *
from datetime import datetime
from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from taggit.models import Tag
from django.db.models import Count
import hashlib

class Achievement():
    slots = ("active", "message", "css_class", "image")
    def __init__(self, num_completed, num_total):
        self.active = True
        if num_completed == 1:
            self.message = "<strong>Congratulations, you've crossed one thing off of your bucket list!</strong> It's just a drop in the bucket though; keep going out and doing more things!"
            self.css_class = "alert-info"
            self.image = "bucket/bucketFull.png"
        elif num_completed == num_total:
            self.message = "<strong>Congratulations, you've completed every item on your bucket list!</strong> Don't rest on your laurels though; add some more things to your list and keep going!"
            self.css_class = "alert-success"
            self.image = "bucket/waterDropBucket.png"
        else:
            self.active = False

def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

def user_profile(request, user_id=None):
    profile_user = User.objects.get(id=user_id)

    enc_email = profile_user.email.strip().lower().encode("utf-8")
    email_hash = hashlib.md5(enc_email).hexdigest()

    user_items = Item.objects.filter(user = profile_user).order_by('completed_date')
    items_completed = Item.objects.filter(user = profile_user).exclude(completed_date__isnull=True)

    num_total = len(user_items)
    num_completed = len(items_completed)

    if num_total == 0:
        num_total = 1

    percentCompleted = ( num_completed / num_total ) * 100
    percentUnCompleted = 100 - percentCompleted

    achievement = Achievement(num_completed, num_total)

    user_tags = Tag.objects.filter(item__user=profile_user).annotate(itemcount=Count('id')).order_by('-itemcount')

    context = {
        'profile_user'        : profile_user,
        'email_hash'          : email_hash,
        'user_items'          : user_items,
        'items_completed'     : items_completed,
        'percent_uncompleted' : percentUnCompleted,
        'percent_completed'   : percentCompleted,
        'user_tags'           : user_tags,
        'achievement'         : achievement,
    }

    return render_to_response("profile.html", context, context_instance=RequestContext(request))

@login_required
def my_profile(request):
    return user_profile(request, user_id=request.user.id)

@login_required
def edit_profile(request):

    user = request.user
    profile = user.profile
    update_success = False

    if request.method == "POST":
        user_form = EditUserForm(request.POST)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = request.user
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.save()
            profile_form.user_id = request.user.id
            profile_form.save()
            update_success = True
            # Allow fallthrough to reload the same screen.
    else:
        user_form = EditUserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {
        'user_form'      : user_form,
        'profile_form'   : profile_form,
        'update_success' : update_success
    }

    return render_to_response("edit_profile.html", context, context_instance=RequestContext(request))

# Create a bucket list item
@login_required
def add_item(request):
    item_form = None
    add_success = False

    if request.method == "POST":
        item_form = ItemForm(request.POST)
        if item_form.is_valid():
            i = item_form.save(commit=False)
            i.user = request.user
            if 'complete' in request.POST:
                i.completed_date = datetime.now()
            i.save()
            item_form.save_m2m()
            add_success = True
    else:
        item_form = ItemForm()
    # TODO process tags
    context = {
        "form"        : item_form,
        "add_success" : add_success,
    }
    return render_to_response('add_item.html', context, context_instance=RequestContext(request))
