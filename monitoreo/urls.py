"""
URL configuration for monitoreo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from dispositivos.views import DeviceListView
from dispositivos.views import  DeviceDetailView
from dispositivos.views import AlertListView
from dispositivos.views import DashboardView
from dispositivos.views import MeasurementListView
from dispositivos.views import WeeklyAlertListView
from dispositivos.forms import OrganizationRegisterForm
from dispositivos.views import OrganizationRegisterView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy









urlpatterns = [
    path('admin/', admin.site.urls),
    path('devices/', DeviceListView.as_view(), name='device_list'),
    path('devices/<int:pk>/', DeviceDetailView.as_view(), name='device_detail'),
    path('alerts/', AlertListView.as_view(), name='alert_list'),  # Nueva ruta para Alertas
    path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Nueva ruta para el Dashboard
    path('measurements/', MeasurementListView.as_view(), name='measurement_list'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('alerts/week/', WeeklyAlertListView.as_view(), name='weekly_alerts'),
    path('register/', OrganizationRegisterView.as_view(), name='register'),
     path('admin/', admin.site.urls),
    path('', include('dispositivos.urls')),
        path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='dispositivos/password_reset.html',
        success_url=reverse_lazy('password_reset_done')
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='dispositivos/password_reset_done.html'
    ), name='password_reset_done'),




]
