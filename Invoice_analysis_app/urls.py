from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'Invoice_analysis_app'
urlpatterns = [
    # Invoice analysis paths
    path('', views.index, name='index'),    
    path('invoiceConvert/', views.invoiceConvert, name='invoiceConvert'),    
    path('DriverEntry/',views.DriverEntry, name='DriverEntry'),
    path('DriverSaveData/',views.DriverSaveData, name='DriverSaveData'),
    
    
    # Trip analysis paths
    path('analysis/', views.analysisView, name='analysis'),
    path('analysis/download/', views.downloadAnalysis, name='downloadAnalysis'),
]
