from django import forms
from location import models as loc_models
from . import models

class GetParentUsernameForm(forms.Form):
    parent_username = forms.CharField()


class AddHealthcarePolicyForm(forms.ModelForm):

    class Meta():
        model = models.HealthcarePolicy
        exclude = ['state']


class GetStateForm(forms.Form):
    state = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(GetStateForm, self).__init__(*args, **kwargs)

        STATE_CHOICES = [(None, '---Select---')]

        state_list = loc_models.State.objects.all()
        for state in state_list:
            STATE_CHOICES.append((state.pk, state.__str__()))


        self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES)