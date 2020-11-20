from django.db import models

# Create your models here.

class MedicalAgency(models.Model):
    user = models.ForeignKey('account.User', related_name='medical_agencies', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.name}'

    class Meta():
        verbose_name_plural = 'Medical Agencies'


class MedicalHelper(models.Model):
    user = models.ForeignKey('account.User', related_name='medical_helpers', on_delete=models.CASCADE)
    medical_agency = models.ForeignKey('medical.MedicalAgency', related_name='medical_helpers', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.medical_agency} -- {self.user.first_name} -- {self.user.last_name}'

    class Meta():
        verbose_name_plural = 'Medical Helpers'

     