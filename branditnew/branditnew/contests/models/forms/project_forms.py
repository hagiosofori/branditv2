from branditnew.contests.models.projects import *
from django import forms

class Create_Project_Form(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'category',
            'description',
            'files',
            'end_date',
        ]

        widgets = {
            'end_date': forms.DateInput(attrs={'type':'date'}),
            'cost' : forms.HiddenInput()
        }

        labels = {
            'category': 'What type of work do you require',
            'description': 'Tell us more about what you want',
            'end_date': 'When do you need it by?',
        }





class Project_Submission_Comment_Form(forms.ModelForm):
    class Meta:
        model = Project_Submission_Comment

        fields = [
            'content',
        ]

        labels = {
            'content': '',
        }

