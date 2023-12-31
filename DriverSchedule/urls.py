"""
URL configuration for DriverSchedule project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from rest_framework import routers
from Trips_details_app import views
from django.contrib import admin
# from run_background_task.views import trigger_exe
# from .views import trigger_exe

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('DriverSchedule_app/', include("DriverSchedule_app.urls")),
    path('Invoice_analysis/', include("Invoice_analysis_app.urls")),
    path('Reconciliation_app/', include("Reconciliation_app.urls")),
    path('Basic_app/', include("Basic_app.urls")),
    path('Trips_details_app/', include("Trips_details_app.urls")),
    # path('run_exe/', trigger_exe),

    # form 1 Log Sheet
    path('static/img/finalLogSheet/<str:logSheet>/', views.viewLogSheet, name="viewLogSheet"),
    path('static/img/docketFiles/<str:docketFile>/', views.viewDocketFile, name="viewDocketFile"),

]
