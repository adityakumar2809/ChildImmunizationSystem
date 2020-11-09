from django.db import models
from django.contrib import auth

# Create your models here.


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return self.username


class StateMedicalOfficer(models.Model):
    user = models.ForeignKey('account.User', related_name='state_medical_officers', on_delete=models.CASCADE)
    state = models.ForeignKey('location.State', related_name='state_medical_officers', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class DistrictMedicalOfficer(models.Model):
    user = models.ForeignKey('account.User', related_name='district_medical_officers', on_delete=models.CASCADE)
    district = models.ForeignKey('location.District', related_name='district_medical_officers', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'