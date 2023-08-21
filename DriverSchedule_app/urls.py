from django.urls import include, path
from rest_framework import routers
from . import views


app_name = 'DriverSchedule_app'
urlpatterns = [
    
    path('index/',views.index,name='index'),
    path('get-driver-data/',views.getDriverData,name='get-driver-data'), 
    
    # Forms url  
    path('getForm1/',views.getForm1,name='form1'),
    path('getForm2/',views.getForm2,name='form2'),
    path('getFileForm/',views.getFileForm,name='getFileForm'),
    path('saveFileForm/',views.saveFileForm,name='saveFileForm'),
    
    
    path('createFormSession/',views.createFormSession,name='createFormSession'),
    
    path('formsSave/',views.formsSave,name='formsSave'),
    
]
