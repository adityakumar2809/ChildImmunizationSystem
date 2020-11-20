from beneficiary import models as ben_models
from data import models as data_models
from location import models as loc_models
from medical import models as med_models

def UserList(request):
    parent_users = [u['user'] for u in ben_models.Parent.objects.all().values('user')]
    medical_agency_users = [u['user'] for u in med_models.MedicalAgency.objects.all().values('user')]
    medical_helper_users = [u['user'] for u in med_models.MedicalHelper.objects.all().values('user')]
    district_medical_officer_users = [u['user'] for u in med_models.DistrictMedicalOfficer.objects.all().values('user')]
    state_medical_officer_users = [u['user'] for u in med_models.StateMedicalOfficer.objects.all().values('user')]

    return {
        'parent_users': parent_users,
        'medical_agency_users': medical_agency_users,
        'medical_helper_users': medical_helper_users,
        'district_medical_officer_users': district_medical_officer_users,
        'state_medical_officer_users': state_medical_officer_users,
    }