from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from . import skills




class SignupForm(UserCreationForm):
    phone_number = forms.CharField(
        required=True,
        max_length=30,
        widget=forms.TextInput()
    )
    # skills = forms.ModelChoiceField(
    #     queryset=skills.objects.all()
    # )
    date_of_birth = forms.DateField(
        help_text='Required. Format: YYYY-MM-DD'
    )


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', ]

