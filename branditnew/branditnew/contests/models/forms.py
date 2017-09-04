from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .contest import Contest
from . import skills
from .entries import Entry



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
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'email', 
            'password', 
            
        ]


class CreateContestForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(CreateContestForm, self).__init__(*args, **kwargs)
    #     # self.fields['client'].queryset=

    class Meta:
        model = Contest
        fields = [
            'client', 
            'title', 
            'about', 
            'prize', 
            'end_date',
            'is_top', 
            'is_hidden', 
            'is_nda', 
            'is_sealed', 
            'cost',
            'category', 
            # 'files',  #file submission still doesn't work. fix it.
        ]

class ContestEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            'contest', #should be set by clicking on the 'submit' for the contest, which leads to this form
            'brandlancer', #should be set by who is logged in
            # 'files',
            'message',
            'sub',
            'boost',
            'hide',
        ]
