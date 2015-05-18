from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    """
    Allows the creation of a new user, with fields:
        - username (additional validation added)
        - first_name
        - last_name
        - email
        - password1
        - password2
    """
    #All fields are required
    username = forms.RegexField(label="Username", max_length=30,
        regex=r'^[a-z0-9.-]+$',
        help_text = "Required. 30 characters or fewer. Lowercase letters, numbers, '.' and '-' only.",
        error_messages = 
        {
            'invalid': "This value may contain only lowercase letters, numbers, '.' and '-'."
        }
    )

    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)

    def clean_username(self):
        reserved_names = ["www", "edit", "id"]

        username = self.cleaned_data["username"]
        for reserved_name in reserved_names:
            if (username == reserved_name):
                raise forms.ValidationError("Invalid user name. Please choose a different name.")
        return username
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
