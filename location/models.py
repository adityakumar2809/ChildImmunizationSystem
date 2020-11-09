from django.db import models

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class District(models.Model):
    state = models.ForeignKey('location.State', related_name='districts', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.state} -- {self.name}'


class Locality(models.Model):
    district = models.ForeignKey('location.District', related_name='localities', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    medical_agency = models.ForeignKey('medical.MedicalAgency', related_name='localities', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.district} -- {self.name}'