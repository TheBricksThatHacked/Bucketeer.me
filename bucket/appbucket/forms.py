from django import forms
from .models import *
from django.core.exceptions import ValidationError

# Create a bucket list item
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ["created_date", "completed_date", "user"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["location", "bio", "gender", "age"]

    def clean_age(self):
        if (int(self.cleaned_data.get('age', 0)) < 0):
            raise ValidationError("Invalid age.")

        return self.cleaned_data.get('age', 0)

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
