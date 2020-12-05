from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import models as auth_models

from beneficiary import models as ben_models
from medical import models as med_models
from location import models as loc_models
from data import models as data_models

import datetime, random, json

def home(request):
    states = loc_models.State.objects.all()
    vaccines = data_models.Vaccine.objects.all()
    vcc_label=[]
    vcc_value=[]
    for vcc in vaccines:
        vaccination_done_count = ben_models.ChildVaccine.objects.all().filter(vaccine__pk__exact=vcc.pk, scheduled_date__lt=datetime.date.today(), is_vaccinated__exact=True).count()
        vaccination_missed_count = ben_models.ChildVaccine.objects.all().filter(vaccine__pk__exact=vcc.pk, scheduled_date__lt=datetime.date.today(), is_vaccinated__exact=False).count()
        if (vaccination_done_count + vaccination_missed_count) > 0:
            vaccinated_percentage = round((vaccination_done_count/(vaccination_done_count + vaccination_missed_count))*100, 2)
        else:
            vaccinated_percentage = 0
        vcc_label.append(vcc.name)
        vcc_value.append(vaccinated_percentage)
    
    
    total_vaccination_done_count = total_vaccination_missed_count = 0
    state_label=[]
    state_value=[]
    time_label=[]
    time_value=[]
    total_label=['Successful', 'Unsuccessful']
    total_value=[]
    for state in states:
        vaccination_done_count = ben_models.ChildVaccine.objects.all().filter(child__parent__locality__district__state__pk__exact=state.pk, scheduled_date__lt=datetime.date.today(), is_vaccinated__exact=True).count()
        vaccination_missed_count = ben_models.ChildVaccine.objects.all().filter(child__parent__locality__district__state__pk__exact=state.pk, scheduled_date__lt=datetime.date.today(), is_vaccinated__exact=False).count()
        if (vaccination_done_count + vaccination_missed_count) > 0:
            vaccinated_percentage = round((vaccination_done_count/(vaccination_done_count + vaccination_missed_count))*100, 2)
        else:
            vaccinated_percentage = 0
        state_label.append(state.name)
        state_value.append(vaccinated_percentage)
        total_vaccination_done_count += vaccination_done_count
        total_vaccination_missed_count += vaccination_missed_count
    total_value.append(total_vaccination_done_count)
    total_value.append(total_vaccination_missed_count)
    
    date_lower_bound = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, 1)
    for _ in range(12):
        date_upper_bound = (date_lower_bound.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) 
        scheduled_vaccines = ben_models.ChildVaccine.objects.all().filter(scheduled_date__gte=date_lower_bound, scheduled_date__lt=date_upper_bound).count()
        time_label.append(f'{date_lower_bound.strftime("%b")}\' {date_lower_bound.strftime("%y")}')
        time_value.append(scheduled_vaccines)
        date_lower_bound = date_upper_bound
    
    data = { "vcc_label": vcc_label, "vcc_value": vcc_value, "state_label": state_label, "state_value": state_value, "time_label": time_label, "time_value": time_value, "total_label": total_label, "total_value": total_value}
    jsondata = json.dumps(data)


    parent_count = ben_models.Parent.objects.all().count()
    children_count = ben_models.Child.objects.all().count()
    medical_agency_count = med_models.MedicalAgency.objects.all().count()
    locality_count = loc_models.Locality.objects.all().count()
    return render(request, 'home.html', {'jsondata':jsondata, 'parent_count':parent_count, 'children_count':children_count, 'medical_agency_count': medical_agency_count, 'locality_count': locality_count})

def fault(request, msg):
    return render(request, 'fault.html', {'msg': msg})

def success(request, msg):
    return render(request, 'success.html', {'msg': msg})

def send_notifications(request):
    notifications = ben_models.Notification.objects.all().filter(is_sent__exact=False, scheduled_date__exact=datetime.date.today())
    for notification in notifications:
        email_list = [notification.child_vaccine.child.parent.user.email, notification.child_vaccine.child.parent.medical_helper.user.email]
        send_mail('Immunization Date Coming Up', f'The Immunization via {notification.child_vaccine.vaccine.name} vaccine for {notification.child_vaccine.child.first_name} is scheduled on {notification.child_vaccine.scheduled_date}. Kindly ensure that the child is getting vaccinated. Thank you', 'myowntestmail0@gmail.com', email_list, fail_silently = True)

    medical_agencies = med_models.MedicalAgency.objects.all()
    for medical_agency in medical_agencies:
        missed_vaccines = ben_models.ChildVaccine.objects.all().filter(child__parent__locality__medical_agency__pk__exact=medical_agency.pk ,scheduled_date__lt=datetime.date.today(), is_vaccinated__exact=False)
        msg_str = 'The following immunizations were skipped in your area and are still not completed: \n'
        for missed_vaccine in missed_vaccines:
            msg_str = msg_str + f'{missed_vaccine.child.parent} -- {missed_vaccine.child} -- { missed_vaccine.vaccine }\n'
            send_mail('Missed Immunization', msg_str, 'myowntestmail0@gmail.com', [medical_agency.user.email], fail_silently = True)
           
    return redirect('home')

def populate(request):
    """ 
    # POPULATE LOCALITIES
    locality_list = ['Jail Chowk', 'Jaankipuram', 'Chandravihar']
    district = loc_models.District.objects.get(name__iexact='Jhansi')
    medical_agency = med_models.MedicalAgency.objects.get(name__iexact='Chiranjeev Hospital')
    for loc in locality_list:
        loc_models.Locality.objects.create(
            district=district,
            name=loc,
            medical_agency=medical_agency
        ) 
    """
    """ 
    # POPULATE MEDICAL HELPERS
    first_names = ['Amar', 'Adarsh', 'Karthik', 'Shyam', 'Rohan', 'Rohit', 'Nitin', 'Mayank', 'Ritesh', 'Piyush', 'Komal', 'Sarita', 'Vineeta', 'Riya', 'Suman', 'Bhavya', 'Jasmine']
    last_names = ['Agarwal', 'Gupta', 'Sharma', 'Verma', 'Sahu', 'Singh', 'Bains', 'Bhatia', 'Chauhan', 'Kapoor', 'Rai', 'Deewan', 'Malhotra', 'Mehra', 'Chaudhary', 'Tripathi']
    medical_agencies = med_models.MedicalAgency.objects.all()
    for med_ag in medical_agencies:
        for _ in range(3):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            user = auth_models.User.objects.create_user(username=f'med-hp-{first_name.lower()}-{last_name.lower()}-{random.randint(111111,999999)}', password='testpassword')
            user.first_name = first_name
            user.last_name = last_name
            user.email = f'{first_name}@{last_name}.com'
            user.save()

            med_models.MedicalHelper.objects.create(user=user, medical_agency=med_ag)
    """
    
    """ 
    # POPULATE DISTRICT MEDICAL OFFICERS
    districts = loc_models.District.objects.all()
    for district in districts:
        if district.name == 'Patiala':
            continue
        first_name = 'District Officer'
        last_name = district.name
        user = auth_models.User.objects.create_user(username=f'med-off-dis-{last_name.lower()}', password='testpassword')
        user.first_name = first_name
        user.last_name = last_name
        user.email = f'{first_name}@{last_name}.com'
        user.save()

        med_models.DistrictMedicalOfficer.objects.create(user=user, district=district)
    """
    
    """ 
    # POPULATE DISTRICT MEDICAL OFFICERS
    states = loc_models.State.objects.all()
    for state in states:
        if state.name == 'Punjab':
            continue
        first_name = 'State Officer'
        last_name = state.name
        user = auth_models.User.objects.create_user(username=f'med-off-sta-{last_name.lower()}', password='testpassword')
        user.first_name = first_name
        user.last_name = last_name
        user.email = f'{first_name}@{last_name}.com'
        user.save()

        med_models.StateMedicalOfficer.objects.create(user=user, state=state)
    """
    
    """ 
    # POPULATE PARENT AND CHILDREN DATA
    localities = loc_models.Locality.objects.all()
    first_names = ['Amar', 'Adarsh', 'Karthik', 'Shyam', 'Rohan', 'Rohit', 'Nitin', 'Mayank', 'Ritesh', 'Piyush', 'Komal', 'Sarita', 'Vineeta', 'Riya', 'Suman', 'Bhavya', 'Jasmine', 'Raman', 'Ajay', 'Mukesh', 'Dharmendra', 'Kunal', 'Amrish', 'Akshay', 'Varun', 'Anuj', 'Divyanshu', 'Ashish', 'Vedant', 'Anay', 'Utkarsh', 'Anoop']
    last_names = ['Agarwal', 'Gupta', 'Sharma', 'Verma', 'Sahu', 'Singh', 'Bains', 'Bhatia', 'Chauhan', 'Kapoor', 'Rai', 'Deewan', 'Malhotra', 'Mehra', 'Chaudhary', 'Tripathi', 'Dwivedi', 'Trivedi', 'Tiwari', 'Saraogi', 'Rawat', 'Yadav', 'Saxena', 'Mishra']
    vaccine_list = data_models.Vaccine.objects.all()
    notification_days_offset = [7,3,1]
    for loc in localities:
        for _ in range(5):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            user = auth_models.User.objects.create_user(username=f'par-{first_name.lower()}-{last_name.lower()}-{random.randint(111111,999999)}', password='testpassword')
            user.first_name = first_name
            user.last_name = last_name
            user.email = f'{first_name}@{last_name}.com'
            user.save()

            medical_agency = loc.medical_agency
            medical_helpers = medical_agency.medical_helpers.all()
            parent = ben_models.Parent.objects.create(user=user, medical_helper=random.choice(medical_helpers), locality=loc)
            for child_count in range(1,4):
                child_dob = datetime.date.today() - datetime.timedelta(days=random.randint(5,300))
                child = ben_models.Child.objects.create(parent=parent, first_name=random.choice(first_names), last_name=last_name, dob=child_dob)
                for vcc in vaccine_list:
                    child_vaccine = ben_models.ChildVaccine.objects.create(child=child, vaccine=vcc, scheduled_date=child_dob + datetime.timedelta(days=vcc.days_offset))
                    for ntf_days_offset in notification_days_offset:
                        ben_models.Notification.objects.create(child_vaccine=child_vaccine, scheduled_date=child_vaccine.scheduled_date - datetime.timedelta(days=ntf_days_offset))
    """

    """
    # ADD EMAIL ADDRESS TO MEDICAL AGENCIES
    medical_agencies = med_models.MedicalAgency.objects.all()
    for med_ag in medical_agencies:
        user = med_ag.user
        user.last_name = 'Hospital'
        user.first_name = med_ag.name.split()[0]
        user.email = f'{med_ag.name.lower().split()[0]}@hospital.com'
        user = user.save()
    """

    """
    # MAKE NOTIFICATION SENT STATUS TRUE
    notifications = ben_models.Notification.objects.all().filter(scheduled_date__lte=datetime.date.today())
    for nt in notifications:
        nt.is_sent = True
        nt.save()
    """

    """
    # MAKE VACCINATION STATUS TRUE
    random_value_choices = [90, 80, 65, 45, 30]
    
    localities = loc_models.Locality.objects.all()
    for loc in localities:
        random_value = random.choice(random_value_choices)
        child_vaccines = ben_models.ChildVaccine.objects.all().filter(scheduled_date__lt=datetime.date.today(), child__parent__locality__pk=loc.pk)
    
        for child_vcc in child_vaccines:
            if random.randint(1,100) < random_value:
                child_vcc.is_vaccinated = True
                child_vcc.save()
    """

    """
    # FIX EMAIL ADDRESSES
    users = auth_models.User.objects.all()
    for user in users:
        user.email = f'{user.first_name.replace(" ","").lower()}@{user.last_name.lower()}.com'
        user.save()
    """

    """
    username = 'par-amit-kumar-567774'
    return redirect('success', msg=f'A new child is registered successfully to parent with username \"{username}\"')
    """

    return redirect('home')