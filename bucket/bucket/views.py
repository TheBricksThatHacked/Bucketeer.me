from django.contrib import auth
from .forms import UserForm
from django.shortcuts import render, redirect


def register(request):

    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            #Next two lines automatically log the user in
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.logout(request)
            auth.login(request, user)
            return redirect('app:edit_profile')
    else:
        user_form = UserForm()

    return render(request, "registration/register.html", {"form" : user_form})

def logout(request):
    """
    This function will attempt to logout. If no user is logged in, then it does
    not error out.
    """
    auth.logout(request)
    return redirect('app:index')
