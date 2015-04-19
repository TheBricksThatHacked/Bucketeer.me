from .models import *
from .forms import *
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseForbidden
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
        'badges'              : get_badges(profile_user),
    }

    return render_to_response("profile.html", context, context_instance=RequestContext(request))

def get_badges(user):
    badges = []

    num_items = Item.objects.filter(user = user).count()
    num_completed = Item.objects.filter(user = user).exclude(completed_date__isnull=True).count()

    # World Traveler 
    #if Item.objects.filter(user = user).exclude(completed_date__isnull=True).tags.filter(tags__name__in = ["travel"]).count() >= 5:
    #    pass
    #badges.append('<span class="label label-success label-lg"><i class="fa fa-trophy"></i> World Traveler</span>')

    # Completionist
    if (num_items >= 10) and (num_completed == num_items):
        badges.append('<span class="label label-info label-lg"><i class="fa fa-bar-chart"></i> Completionist</span>')

    # Newbie
    if (num_items < 3):
        badges.append('<span class="label label-success label-lg"><i class="fa fa-child"></i> Newbie</span>')

    # Intermediate
    if (num_items >= 3) and (num_items <= 25):
        badges.append('<span class="label label-warning label-lg"><i class="fa fa-graduation-cap"></i> Intermediate</span>')

    # Hardcore
    if (num_items > 25):
        badges.append('<span class="label label-danger label-lg"><i class="fa fa-diamond"></i> Hardcore</span>')

    # Big Bucket
    if (num_items > 50) and (num_completed > (num_items / 2)):
        badges.append('<span class="label label-danger label-lg"><i class="fa fa-bitbucket"></i> Big Bucket</span>')

    # Top 10%

    # 50-50
    if (num_completed == int(num_items / 2)):
        badges.append('<span class="label label-info label-lg"><i class="fa fa-adjust"></i> 50-50</span>')

    # X Year Club
    years_passed = ((datetime.now() - User.objects.filter(id = user.id).datetimes("date_joined", "hour")[0]).days // 365)
    if (years_passed) > 1:
    #    years_passed club
        badges.append('<span class="label label-default label-lg"><i class="fa fa-trophy"></i> {0} Year Club</span>'.format(years_passed))

    # Dreamer
    if (num_items > 10) and (num_completed / num_items) < 0.1:
        badges.append('<span class="label label-default label-lg"><i class="fa fa-bed"></i> Dreamer</span>')

    # Bucket Day
    if (User.objects.filter(id = user.id).datetimes("date_joined", "day")[0].replace(year=2000).date()) == datetime.now().replace(year=2000).date():
        badges.append('<span class="label label-info label-lg"><i class="fa fa-birthday-cake"></i> Bucket Day</span>')

    return badges


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

@login_required
def edit_item(request, item_id=None):
    i = get_object_or_404(Item, pk=item_id)
    if (i.user.id != request.user.id):
        return HttpResponseForbidden("You do not have access to that item")
    item_form = None
    if request.method == "POST":
        item_form = ItemForm(request.POST, instance=i)
        if item_form.is_valid():
            i = item_form.save(commit=False)
            i.save()
            item_form.save_m2m()
            return redirect("app:my_profile")
    else:
        item_form = ItemForm(instance=i)

    context = {
        "form" : item_form,
    }
    return render_to_response('add_item.html', context, context_instance=RequestContext(request))
