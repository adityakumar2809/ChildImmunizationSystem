from django.db import models

# Create your models here.

class MedicalAgency(models.Model):
    user = models.ForeignKey('account.User', related_name='medical_agencies', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.name}'

     