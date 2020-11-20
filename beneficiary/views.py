from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models as auth_models
from account import forms as acc_forms
from medical import models as med_models
from location import models as loc_models
from data import models as data_models

import random, string, datetime

from . import models, forms

# Create your views here.

def signup_parent(request):
    if request.method == 'POST':
        form = acc_forms.UserCreateForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                return redirect('fault', fault='Username/Email already exists!')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return redirect('fault', fault='Invalid Request')

            return redirect('home')
        else:
            return redirect('fault', msg='Username or Email already exists!')
    else:
        form = acc_forms.UserCreateForm()
        return render(request, 'beneficiary/signup-parent.html', {'form' : form})


@login_required
def create_parent(request):
    if request.method == 'POST':
        form = forms.ParentCreationForm(data=request.POST, user=request.user)
        if form.is_valid():
            parent_first_name = form.cleaned_data['parent_first_name']
            parent_last_name = form.cleaned_data['parent_last_name']
            parent_email = form.cleaned_data['parent_email']
            locality = form.cleaned_data['locality']
            helper = form.cleaned_data['helper']
            child_first_name = form.cleaned_data['child_first_name']
            child_last_name = form.cleaned_data['child_last_name']
            child_dob = form.cleaned_data['child_dob']

            username = f'par-{parent_first_name.lower()}-{random.randint(111111,999999)}'
            password = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(8)))
            user = auth_models.User.objects.create_user(username=username, password=password)
            user.first_name = parent_first_name
            user.last_name = parent_last_name
            user.email = parent_email
            user.save()
            if user is not None:
                parent = models.Parent.objects.create(user=user, medical_helper=med_models.MedicalHelper.objects.get(pk__exact=helper), locality=loc_models.Locality.objects.get(pk__exact=locality))
                child = models.Child.objects.create(parent=parent, first_name=child_first_name, last_name=child_last_name, dob=child_dob)

                vaccine_list = data_models.Vaccine.objects.all()
                for vcc in vaccine_list:
                    models.ChildVaccine.objects.create(child=child, vaccine=vcc, scheduled_date=child_dob + datetime.timedelta(days=vcc.days_offset))

                return redirect('home')
            else:
                return redirect('fault', fault='Invalid Request')

        else:
            return redirect('fault', msg='Error Occurred')
    else:
        form = forms.ParentCreationForm(user=request.user)
        return render(request, 'beneficiary/create-parent.html', {'form': form})