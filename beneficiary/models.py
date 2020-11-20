from django.db import models
from django.contrib import auth

# Create your models here.


class Parent(models.Model):
    user = models.ForeignKey(auth.models.User, related_name='parents', on_delete=models.CASCADE)
    medical_helper = models.ForeignKey('medical.MedicalHelper', related_name='parents', on_delete=models.CASCADE)
    locality = models.ForeignKey('location.Locality', related_name='parents', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Child(models.Model):
    parent = models.ForeignKey('beneficiary.Parent', related_name='children', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta():
        verbose_name_plural = 'Children'
