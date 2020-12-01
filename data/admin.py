from django.contrib import admin
from . import models

# Register your models here.

class VaccineAdmin(admin.ModelAdmin):
    list_display = ('name', 'days_offset')

admin.site.register(models.Vaccine, VaccineAdmin)