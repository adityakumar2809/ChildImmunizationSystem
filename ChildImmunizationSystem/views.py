from django.shortcuts import render, redirect
from django.core.mail import send_mail

from beneficiary import models as ben_models

import datetime

def home(request):
    return render(request, 'home.html', {})

def fault(request, msg):
    return render(request, 'fault.html', {'msg': msg})

def send_notifications(request):
    notifications = ben_models.Notification.objects.all().filter(is_sent__exact=False, scheduled_date__exact=datetime.date.today())
    for notification in notifications:
        email_list = [notification.child_vaccine.child.parent.user.email, notification.child_vaccine.child.parent.medical_helper.user.email]
        send_mail('Immunization Date Coming Up', f'The Immunization via {notification.child_vaccine.vaccine.name} vaccine for {notification.child_vaccine.child.first_name} is scheduled on {notification.child_vaccine.scheduled_date}. Kindly ensure that the child is getting vaccinated. Thank you', 'myowntestmail0@gmail.com', email_list, fail_silently = True)
    return redirect('home')