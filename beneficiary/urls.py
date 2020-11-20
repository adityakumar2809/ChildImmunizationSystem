from django.urls import path

from . import views

app_name = 'beneficiary'

urlpatterns = [
    path('signup-parent/', views.signup_parent, name='signup_parent'),
    path('create-parent/', views.create_parent, name='create_parent'),
    path('list-children/<int:pk>/', views.list_children, name='list_children'),
]