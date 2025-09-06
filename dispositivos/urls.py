from django.urls import path
from dispositivos.views import DashboardView, OrganizationRegisterView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('register/', OrganizationRegisterView.as_view(), name='register'),
]