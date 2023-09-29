from django.urls import include, path
from rest_framework import routers
from . import views

app_name = 'Invoice_analysis_app'
urlpatterns = [
    path('', views.index, name='index'),    
    path('invoiceConvert/', views.invoiceConvert, name='invoiceConvert'),    
]
