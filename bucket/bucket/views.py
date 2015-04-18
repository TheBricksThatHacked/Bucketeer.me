from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register(request):

    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            #Next two lines automatically log the user in
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.logout(request)
            auth.login(request, user)
            return redirect('app:user_profile', user_id=user.id)
    else:
        user_form = UserCreationForm()

    return render(request, "registration/register.html", {"form" : user_form})