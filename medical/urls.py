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
    path('district-medical-officer-analysis-locality-wise/', views.district_medical_officer_analysis_locality_wise, name='district_medical_officer_analysis_locality_wise'),   
    path('district-medical-officer-analysis-parent-wise/<int:pk>/', views.district_medical_officer_analysis_parent_wise, name='district_medical_officer_analysis_parent_wise'),
    path('state-medical-officer-analysis-district-wise/', views.state_medical_officer_analysis_district_wise, name='state_medical_officer_analysis_district_wise'),
    path('state-medical-officer-analysis-locality-wise/<int:pk>/', views.state_medical_officer_analysis_locality_wise, name='state_medical_officer_analysis_locality_wise'),
    path('state-medical-officer-analysis-parent-wise/<int:pk>/', views.state_medical_officer_analysis_parent_wise, name='state_medical_officer_analysis_parent_wise'),
    path('add-healthcare-policy/', views.add_healthcare_policy, name='add_healthcare_policy'),
    path('list-healthcare-policy/', views.list_healthcare_policy, name='list_healthcare_policy'),
    path('detail-healthcare-policy/<int:pk>/', views.detail_healthcare_policy, name='detail_healthcare_policy'),
]