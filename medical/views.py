from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from beneficiary import models as ben_models

from . import models, forms

import datetime, json
# Create your views here.

@login_required
def list_children(request):
    if request.method == 'POST':
        form = forms.GetParentUsernameForm(data=request.POST)
        if form.is_valid():
            parent_username = form.cleaned_data['parent_username']

            try:
                parent = ben_models.Parent.objects.get(user__username__exact=parent_username)
            except:
                return redirect('fault', msg='Invalid Username entered')
            if parent.locality.medical_agency.user.pk == request.user.pk:
                children_list = parent.children.all()
                form = forms.GetParentUsernameForm()
                return render(request, 'medical/list-children.html', {'children_list':children_list, 'form': form}) 
            else:
                return redirect('fault', msg='The given parent does not reside in your area of operation')
        else:
            return redirect('fault', msg='Invalid Request')
    else:
        form = forms.GetParentUsernameForm()
        return render(request, 'medical/list-children.html', {'form':form})


@login_required
def detail_children(request, pk):
    child = ben_models.Child.objects.get(pk__exact=pk)
    if request.user.pk == child.parent.locality.medical_agency.user.pk:
        vaccination_status_list = child.child_vaccines.all()
        return render(request, 'medical/detail-children.html', {'vaccination_status_list':vaccination_status_list})
    else:
        return redirect('fault', msg='ACCESS DENIED!')


@login_required
def toggle_child_vaccination_status(request, pk):
    child_vaccine = ben_models.ChildVaccine.objects.get(pk__exact=pk)
    child = child_vaccine.child
    if request.user.pk == child.parent.locality.medical_agency.user.pk:
        child_vaccine.is_vaccinated = not(child_vaccine.is_vaccinated)
        child_vaccine.save()
        vaccination_status_list = child.child_vaccines.all()
        return render(request, 'medical/detail-children.html', {'vaccination_status_list':vaccination_status_list})
    else:
        return redirect('fault', msg='ACCESS DENIED!')

@login_required
def list_children_medical_helper(request):
    if request.method == 'POST':
        form = forms.GetParentUsernameForm(data=request.POST)
        if form.is_valid():
            parent_username = form.cleaned_data['parent_username']

            try:
                parent = ben_models.Parent.objects.get(user__username__exact=parent_username)
            except:
                return redirect('fault', msg='Invalid Username entered')
            if parent.medical_helper.user.pk == request.user.pk:
                children_list = parent.children.all()
                form = forms.GetParentUsernameForm()
                return render(request, 'medical/list-children-medical-helper.html', {'children_list':children_list, 'form': form}) 
            else:
                return redirect('fault', msg='The given parent does not reside in your area of operation')
        else:
            return redirect('fault', msg='Invalid Request')
    else:
        form = forms.GetParentUsernameForm()
        return render(request, 'medical/list-children-medical-helper.html', {'form':form})


@login_required
def detail_children_medical_helper(request, pk):
    child = ben_models.Child.objects.get(pk__exact=pk)
    if child.parent.medical_helper.user.pk == request.user.pk:
        vaccination_status_list = child.child_vaccines.all()
        return render(request, 'medical/detail-children-medical-helper.html', {'vaccination_status_list':vaccination_status_list})
    else:
        return redirect('fault', msg='ACCESS DENIED!')


@login_required
def medical_agency_analysis_locality_wise(request):
    medical_agency = models.MedicalAgency.objects.get(user__pk__exact=request.user.pk)
    locality_list = medical_agency.localities.all()
    locality_wise_vaccination_status = []
    label = []
    value = []
    for locality in locality_list:
        vaccination_done_count = vaccination_missed_count = 0
        parents = locality.parents.all()
        for parent in parents:
            children = parent.children.all()
            for child in children:
                vaccination_done_count += ben_models.ChildVaccine.objects.all().filter(child__exact=child, scheduled_date__lte=datetime.date.today(), is_vaccinated__exact=True).count()
                vaccination_missed_count += ben_models.ChildVaccine.objects.all().filter(child__exact=child, scheduled_date__lte=datetime.date.today(), is_vaccinated__exact=False).count()
        if (vaccination_done_count + vaccination_missed_count) > 0:
            vaccinated_percentage = vaccination_done_count/(vaccination_done_count + vaccination_missed_count)
        else:
            vaccinated_percentage = 0
        label.append(locality.name)
        value.append(vaccinated_percentage)
        locality_wise_vaccination_status.append({'locality':locality.name, 'vaccination_done_count':vaccination_done_count, 'vaccination_missed_count':vaccination_missed_count, 'vaccinated_percentage':vaccinated_percentage})
    data = { "label": label, "value": value}
    jsondata = json.dumps(data)
    return render(request, 'medical/medical-agency-analysis-locality-wise.html', {'locality_wise_vaccination_status':locality_wise_vaccination_status, 'jsondata':jsondata})
        