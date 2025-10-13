from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Vehicle, Upgrade


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TuningForm(forms.Form):
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all(), label="Select Vehicle")
    upgrade = forms.ModelChoiceField(queryset=Upgrade.objects.all(), label="Select Upgrade")



