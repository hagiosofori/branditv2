from django import forms

from branditnew.contests.models.print_orders import Item, Print_Order


class Create_Print_Order_Form(forms.ModelForm):
    class Meta:
        model = Print_Order
        fields = [
            'uploaded_design',
            'quantity',
        ]

        labels = {
            'uploaded_design': '',
            'quantity': 'How many pieces would you like to print?',
        }

