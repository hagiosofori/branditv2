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
            'title',
            'end_date',
            'prize',
            'is_top',
            'is_hidden',
            'is_nda',
            'is_sealed',
            'cost',
            'category',
            'preferred_style',
            'preferred_colors',
            'target_audience',
            'design_details',
            'would_like_to_print',
            # 'files',  #file submission still doesn't work. fix it.
            'logo',
            'sketch',
            'files',
        ]
        widgets = {
            'cost': forms.HiddenInput(),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            # 'preferred_colors': forms.TextInput(attrs={'type': 'color'}),
            
        }
        
        labels = {
            'title': "Give a title to your contest",
            'end_date': "When should the contest end?",
            'prize': 'What is your contest award?',
            'category': 'What do you want designed?',
            'target_audience': 'Describe the target audience of the design',
            'preferred_style': 'Describe the style you prefer',
            'preferred_colors': 'Describe your preferred colors',
            'design_details': 'Describe any details you want on the design',
            'would_like_to_print': 'Would you like to print after the contest is completed?',
            'is_top': '',
            'is_hidden': '',
            'is_nda': '',
            'is_sealed': '',
            'logo': 'Upload a logo you want to include in the design [Optional]',
            'sketch': 'Upload a sketch or image that would help explain your request [Optional]',
        }

        help_texts = {
            'end_date': 'Minimum is 3 days from today',
            'prize': 'Minimum prize amount is GHS300',
            
        }


class ContestEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            # 'contest',  # should be set by clicking on the 'submit' for the contest, which leads to this form
            # 'brandlancer',  # should be set by who is logged in
            'title',
            'files',
            'message',
            'sub',
            'boost',
            'hide',
            'cost',
        ]

        labels = {
            'files': 'File',
            'sub': '',
            'boost': '',
            'hide': '',
        }

        widgets = {
            'cost': forms.HiddenInput(),
        }


class SignInForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
