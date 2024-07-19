from django import forms
from django.contrib.auth.models import User
import re

class Signup(forms.ModelForm):
    username = forms.CharField(max_length=60)
    def clean(self):
        total_data = super().clean()
        user_name = total_data["username"]
        p1 = re.fullmatch(r'[a-zA-Z0-9]+',str(user_name))
        if not p1:
            raise forms.ValidationError("No special Characters allowed in Username")
    class Meta:
        model = User
        fields = ["username","password","email","first_name","last_name"]
class Trip_form(forms.Form):
    from_add = forms.CharField(max_length=100,label="From")
    to_add = forms.CharField(max_length=100, label="To")
class Search_form(forms.Form):
    place = forms.CharField(max_length=100,label="Place")
    area = forms.CharField(max_length=100,label="Type of area")
