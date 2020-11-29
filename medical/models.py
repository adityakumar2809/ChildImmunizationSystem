from django.db import models
from django.contrib import auth

# Create your models here.

class StateMedicalOfficer(models.Model):
    user = models.ForeignKey(auth.models.User, related_name='state_medical_officers', on_delete=models.CASCADE)
    state = models.ForeignKey('location.State', related_name='state_medical_officers', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta():
        verbose_name_plural = 'State Medical Officers'


class DistrictMedicalOfficer(models.Model):
    user = models.ForeignKey(auth.models.User, related_name='district_medical_officers', on_delete=models.CASCADE)
    district = models.ForeignKey('location.District', related_name='district_medical_officers', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta():
        verbose_name_plural = 'District Medical Officers'


class MedicalAgency(models.Model):
    user = models.ForeignKey(auth.models.User, related_name='medical_agencies', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.name}'

    class Meta():
        verbose_name_plural = 'Medical Agencies'


class MedicalHelper(models.Model):
    user = models.ForeignKey(auth.models.User, related_name='medical_helpers', on_delete=models.CASCADE)
    medical_agency = models.ForeignKey('medical.MedicalAgency', related_name='medical_helpers', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.medical_agency} -- {self.user.first_name} {self.user.last_name}'

    class Meta():
        verbose_name_plural = 'Medical Helpers'


class HealthcarePolicy(models.Model):
    state = models.ForeignKey('location.State', related_name='healthcare_policies', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    eligibility = models.TextField()
    process = models.TextField()

    def __str__(self):
        return f'{self.state} -- {self.title}'

    class Meta():
        verbose_name_plural = 'Healthcare Policies'

     