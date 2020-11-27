from django.urls import path

from . import views

app_name = 'medical'

urlpatterns = [
    path('list-children/', views.list_children, name='list_children'),    
    path('detail-children/<int:pk>/', views.detail_children, name='detail_children'),
    path('toggle-child-vaccination-status/<int:pk>/', views.toggle_child_vaccination_status, name='toggle_child_vaccination_status'),
]