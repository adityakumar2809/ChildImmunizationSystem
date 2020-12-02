from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models as auth_models
from django.core.mail import send_mail
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
                return redirect('fault', msg='Username/Email already exists!')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                return redirect('fault', msg='Invalid Request')

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

            username = f'par-{parent_first_name.lower()}-{parent_last_name.lower()}-{random.randint(111111,999999)}'
            password = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(8)))
            user = auth_models.User.objects.create_user(username=username, password=password)
            user.first_name = parent_first_name
            user.last_name = parent_last_name
            user.email = parent_email
            user.save()
            if user is not None:
                parent = models.Parent.objects.create(user=user, medical_helper=med_models.MedicalHelper.objects.get(pk__exact=helper), locality=loc_models.Locality.objects.get(pk__exact=locality))
                child = models.Child.objects.create(parent=parent, first_name=child_first_name, last_name=child_last_name, dob=child_dob)
                send_mail('New Parent Registration', f'Your account is initiated on the portal. Please access it using USERNAME - {username} and PASSWORD - {password}. Thank you.', 'myowntestmail0@gmail.com', [parent_email], fail_silently = True)
                vaccine_list = data_models.Vaccine.objects.all()
                notification_days_offset = [7,3,1]
                for vcc in vaccine_list:
                    child_vaccine = models.ChildVaccine.objects.create(child=child, vaccine=vcc, scheduled_date=child_dob + datetime.timedelta(days=vcc.days_offset))
                    for ntf_days_offset in notification_days_offset:
                        models.Notification.objects.create(child_vaccine=child_vaccine, scheduled_date=child_vaccine.scheduled_date - datetime.timedelta(days=ntf_days_offset))

                return redirect('home')
            else:
                return redirect('fault', msg='Invalid Request')

        else:
            return redirect('fault', msg='Error Occurred')
    else:
        form = forms.ParentCreationForm(user=request.user)
        return render(request, 'beneficiary/create-parent.html', {'form': form})


@login_required
def add_child_to_parent(request):
    if request.method == 'POST':
        form = forms.ChildAdditionForm(data=request.POST)
        if form.is_valid():
            parent_username = form.cleaned_data['parent_username']
            child_first_name = form.cleaned_data['child_first_name']
            child_last_name = form.cleaned_data['child_last_name']
            child_dob = form.cleaned_data['child_dob']

            try:
                parent = models.Parent.objects.get(user__username__exact=parent_username)
            except:
                return redirect('fault', msg='Invalid Username entered')
            if parent.locality.medical_agency.user.pk == request.user.pk:
                child = models.Child.objects.create(parent=parent, first_name=child_first_name, last_name=child_last_name, dob=child_dob)
                vaccine_list = data_models.Vaccine.objects.all()
                notification_days_offset = [7,3,1]
                for vcc in vaccine_list:
                    child_vaccine = models.ChildVaccine.objects.create(child=child, vaccine=vcc, scheduled_date=child_dob + datetime.timedelta(days=vcc.days_offset))
                    for ntf_days_offset in notification_days_offset:
                        models.Notification.objects.create(child_vaccine=child_vaccine, scheduled_date=child_vaccine.scheduled_date - datetime.timedelta(days=ntf_days_offset))
                return redirect('home')
            else:
                return redirect('fault', msg='The given parent does not reside in your area of operation')
        else:
            return redirect('fault', msg='Invalid Request')
    else:
        form = forms.ChildAdditionForm()
        return render(request, 'beneficiary/add-child-to-parent.html', {'form':form})


@login_required
def list_children(request, pk):
    if (request.user.pk == pk):
        children_list = models.Parent.objects.get(user__exact=pk).children.all()
        return render(request, 'beneficiary/list-children.html', {'children_list':children_list})
    else:
        return redirect('fault', msg='ACCESS DENIED!')


@login_required
def detail_children(request, pk):
    child = models.Child.objects.get(pk__exact=pk)
    if request.user.pk == child.parent.user.pk:
        vaccination_status_list = child.child_vaccines.all()
        return render(request, 'beneficiary/detail-children.html', {'vaccination_status_list':vaccination_status_list})
    else:
        return redirect('fault', msg='ACCESS DENIED!')


@login_required
def detail_medical(request, pk):
    if request.user.pk == pk:
        parent = models.Parent.objects.get(user__exact=pk)
        medical_helper = med_models.MedicalHelper.objects.get(pk__exact=parent.medical_helper.pk)
        medical_agency = med_models.MedicalAgency.objects.get(pk__exact=medical_helper.medical_agency.pk)
        return render(request, 'beneficiary/detail-medical.html', {'medical_agency':medical_agency, 'medical_helper':medical_helper})
    else:
        return redirect('fault', msg='ACCESS DENIED!')