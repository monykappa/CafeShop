# forms.py
from django import forms

class UserDetailForm(forms.Form):
    location = forms.CharField(max_length=300, required=True)
    contact = forms.CharField(max_length=20, required=True)
