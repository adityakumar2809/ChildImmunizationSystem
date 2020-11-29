from django import forms
from . import models

class GetParentUsernameForm(forms.Form):
    parent_username = forms.CharField()

class AddHealthcarePolicyForm(forms.ModelForm):

    class Meta():
        model = models.HealthcarePolicy
        exclude = ['state']
