from django.contrib.auth.forms import AuthenticationForm

def include_login_form(request):
    form = AuthenticationForm()
    return {'login_form': form, 'test': "TEST"}
