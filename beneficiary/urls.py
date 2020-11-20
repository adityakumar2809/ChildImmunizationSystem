from django.urls import path

from . import views

app_name = 'beneficiary'

urlpatterns = [
    path('signup-parent/', views.signup_parent, name='signup_parent'),
]