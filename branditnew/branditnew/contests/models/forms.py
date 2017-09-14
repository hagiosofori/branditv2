from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets

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
        help_text='Required. Format: YYYY-MM-DD', widget=forms.TextInput(attrs={'class': 'datepicker'})
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
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
            'end_date',
            'about',
            'prize',
            'is_top',
            'is_hidden',
            'is_nda',
            'is_sealed',
            'cost',
            'category',
            # 'files',  #file submission still doesn't work. fix it.
        ]
        widgets = {
            'client': forms.HiddenInput(),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
        labels = {
            'title': "Give a title to your contest",
            'end_date': "When should the contest end?",

        }


class ContestEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            'contest',  # should be set by clicking on the 'submit' for the contest, which leads to this form
            'brandlancer',  # should be set by who is logged in
            # 'files',
            'message',
            'sub',
            'boost',
            'hide',
        ]


class SignInForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
