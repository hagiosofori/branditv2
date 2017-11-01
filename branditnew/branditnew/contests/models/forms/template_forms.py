from django import forms

from ..templates import Template_Order



class Template_Order_Form(forms.ModelForm):
    class Meta:
        model = Template_Order

        fields = [
            'quantity',
            'changes',

        ]

        labels = {
            'quantity': 'How many copies would you like to print',
            'changes': 'Please specify any changes you would like to make to the template',
        }

    
