from django import forms
from .models import *

# Create a bucket list item
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ["created_date", "completed_date", "user"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["location", "bio", "gender"]

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
