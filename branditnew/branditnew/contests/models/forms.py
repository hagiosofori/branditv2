from django.forms import ModelForm
from . import Brandit_user


class SignupForm(ModelForm):
    class Meta:
        model = Brandit_user
        fields = []