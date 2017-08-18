from django import forms
from . import profiles
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    date_of_birth = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    
      
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', ]
