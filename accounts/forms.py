from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.template.defaultfilters import register
from accounts.models import User
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", 'last_name', "gender", "date_of_birth")


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())