from django.urls import include, path
from rest_framework import routers
from . import views


app_name = 'Reconciliation_app'
urlpatterns = [
    # Invoice analysis paths
    path('', views.index, name='index'),    
    path('reconciliation', views.reconciliation, name='reconciliation'),    
   
]
