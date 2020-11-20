from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.StateMedicalOfficer)
admin.site.register(models.DistrictMedicalOfficer)