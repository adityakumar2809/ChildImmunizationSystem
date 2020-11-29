from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.StateMedicalOfficer)
admin.site.register(models.DistrictMedicalOfficer)
admin.site.register(models.MedicalAgency)
admin.site.register(models.MedicalHelper)
admin.site.register(models.HealthcarePolicy)
