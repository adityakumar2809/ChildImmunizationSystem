from django import forms

class GetParentUsernameForm(forms.Form):
    parent_username = forms.CharField()
