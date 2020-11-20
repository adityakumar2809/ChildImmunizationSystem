from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from account import forms as acc_forms

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
            print(form)
        else:
            return redirect('fault', msg='Error Occurred')
    else:
        form = forms.ParentCreationForm(user=request.user)
        return render(request, 'beneficiary/create-parent.html', {'form': form})