from django.urls import include, path
from rest_framework import routers
from . import views


app_name = 'Trips_details_app'
urlpatterns = [

    path('index/', views.index, name='index'),

    # Driver-trip Forms url
    path('getForm1/', views.getForm1, name='form1'),
    path('getForm2/', views.getForm2, name='form2'),
    path('createFormSession/', views.createFormSession, name='createFormSession'),
    path('formsSave/', views.formsSave, name='formsSave'),

    
    path('getTrucks/', views.getTrucks, name="getTrucks"),
    path('clientDocket/', views.clientDocket, name="clientDocket"),
    
    
    # Past data entry 
    path('pastDataEntry/view/', views.pastDataEntryView, name="pastDataEntryView"),
    path('pastDataEntry/save/', views.pastDataEntrySave, name="pastDataEntrySave"),
    
    
]
