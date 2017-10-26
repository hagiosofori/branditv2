from django import forms

from ..projects import Project_Submission


class Make_Project_Submission_Form(forms.ModelForm):
    class Meta: 
        model = Project_Submission
        fields = [
            'title',
            'submission',
            'price',
        ]
        