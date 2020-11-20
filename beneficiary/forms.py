from django import forms

from medical import models as med_models

class ParentCreationForm(forms.Form):
    parent_first_name = forms.CharField()
    parent_last_name = forms.CharField()
    parent_email = forms.EmailField()
    locality = forms.ChoiceField(choices=[])
    helper = forms.ChoiceField(choices=[])
    child_first_name = forms.CharField()
    child_last_name = forms.CharField()
    child_dob = forms.DateField()

    def __init__(self, user, *args, **kwargs):
        super(ParentCreationForm, self).__init__(*args, **kwargs)

        LOCALITY_CHOICES = []
        HELPER_CHOICES = []

        localities_list = med_models.MedicalAgency.objects.get(user__exact=user.pk).localities.all()
        for loc in localities_list:
            LOCALITY_CHOICES.append((loc.pk, loc.__str__()))
        
        helper_list = med_models.MedicalAgency.objects.get(user__exact=user.pk).medical_helpers.all()
        for hp in helper_list:
            HELPER_CHOICES.append((hp.pk, hp.__str__()))

        self.fields['locality'] = forms.ChoiceField(choices=LOCALITY_CHOICES)
        self.fields['helper'] = forms.ChoiceField(choices=HELPER_CHOICES)