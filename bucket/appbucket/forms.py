from django import forms
from .models import *

# Create a bucket list item
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ["created_date", "completed_date", "user"]