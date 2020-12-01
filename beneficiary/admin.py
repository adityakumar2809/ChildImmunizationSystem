from django.contrib import admin
from . import models

# Register your models here.


class ParentAdmin(admin.ModelAdmin):
    list_display = ('parent', 'username', 'state', 'district', 'locality', 'medical_agency', 'medical_helper')

    def parent(self, obj):
        return obj.__str__()

    def username(self, obj):
        return str(obj.user.username)

    def state(self, obj):
        return str(obj.locality.district.state.name)

    def district(self, obj):
        return str(obj.locality.district.name)

    def locality(self, obj):
        return str(obj.locality.name)

    def medical_agency(self, obj):
        return str(obj.locality.medical_agency.name)

    def medical_helper(self, obj):
        return str(obj.medical_helper.user.first_name)



class ChildAdmin(admin.ModelAdmin):
    list_display = ('child', 'parent', 'state', 'district', 'locality', 'medical_agency', 'dob')

    def child(self, obj):
        return obj.__str__()

    def username(self, obj):
        return str(obj.parent.user.username)

    def state(self, obj):
        return str(obj.parent.locality.district.state.name)

    def district(self, obj):
        return str(obj.parent.locality.district.name)

    def locality(self, obj):
        return str(obj.parent.locality.name)

    def medical_agency(self, obj):
        return str(obj.parent.locality.medical_agency.name)



class ChildVaccineAdmin(admin.ModelAdmin):
    list_display = ('child', 'vaccine', 'scheduled_date', 'is_vaccinated')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('child', 'vaccine', 'scheduled_date', 'is_sent')

    def child(self, obj):
        return str(obj.child_vaccine.child)
    
    def vaccine(self, obj):
        return str(obj.child_vaccine.vaccine)


admin.site.register(models.Parent, ParentAdmin)
admin.site.register(models.Child, ChildAdmin)
admin.site.register(models.ChildVaccine, ChildVaccineAdmin)
admin.site.register(models.Notification, NotificationAdmin)