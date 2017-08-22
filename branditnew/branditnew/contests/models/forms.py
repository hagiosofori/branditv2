from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from . import skills




class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        required=True,
        max_length=30,
        widget=forms.TextInput()
    )
    # skills = forms.ModelChoiceField(
    #     queryset=skills.objects.all()
    # )
    birth_date = forms.DateField(
        help_text='Required. Format: YYYY-MM-DD'
    )


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', ]
