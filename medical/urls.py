from django.urls import path

from . import views

app_name = 'medical'

urlpatterns = [
    path('list-children/', views.list_children, name='list_children'),    
    path('detail-children/<int:pk>/', views.detail_children, name='detail_children'),
    path('toggle-child-vaccination-status/<int:pk>/', views.toggle_child_vaccination_status, name='toggle_child_vaccination_status'),
    path('list-children-medical-helper/', views.list_children_medical_helper, name='list_children_medical_helper'),    
    path('detail-children-medical-helper/<int:pk>/', views.detail_children_medical_helper, name='detail_children_medical_helper'),
    path('medical-agency-analysis-locality-wise/', views.medical_agency_analysis_locality_wise, name='medical_agency_analysis_locality_wise'),
    path('medical-agency-analysis-parent-wise/<int:pk>/', views.medical_agency_analysis_parent_wise, name='medical_agency_analysis_parent_wise'),
]