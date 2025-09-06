from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic import DetailView
from django.views.generic import TemplateView
from dispositivos.models import Device, Measurement,AlertProduct,Category
from dispositivos.models import Measurement
from django.utils.timezone import now, timedelta
from .models import AlertProduct
from .models import Device
from django.db.models import Count
from django.urls import reverse_lazy
from datetime import timedelta
from django.utils import timezone
from dispositivos.forms import OrganizationRegisterForm
from django.urls import reverse_lazy







class DeviceListView(ListView):
    model = Device
    template_name = 'dispositivos/device_list.html'
    context_object_name = 'devices'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(id_cat_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        return context


class DeviceDetailView(DetailView):
    model = Device
    template_name = 'dispositivos/device_detail.html'
    context_object_name = 'device'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.get_object()

        # Mediciones ordenadas por fecha descendente
        context['measurements'] = Measurement.objects.filter(idProd=device).order_by('-created_at')

        # Alertas asociadas al dispositivo
        context['alerts'] = AlertProduct.objects.filter(id_prod=device.id_prod).select_related('id_alert')
        print(type(device.id_prod))
        return context


class AlertListView(ListView):
    model = AlertProduct
    template_name = 'dispositivos/alert_list.html'
    context_object_name = 'alerts'

    def get_queryset(self):
        return AlertProduct.objects.select_related('id_alert', 'id_prod').all()

class DashboardView(TemplateView):
    template_name = 'dispositivos/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_devices'] = Device.objects.count()
        context['active_devices'] = Device.objects.filter(estado='ACTIVO').count()
        context['critical_alerts'] = AlertProduct.objects.filter(id_alert__severity='Alto').count()
        context['estimated_savings'] = Device.objects.filter(estado='INACTIVO').count() * 15  # ejemplo: 15 kWh por dispositivo apagado
        return context

class MeasurementListView(ListView):
    model = Measurement
    template_name = 'dispositivos/measurement_list.html'
    context_object_name = 'measurements'
    paginate_by = 50
    ordering = ['-timestamp']

    def get_queryset(self):
        return Measurement.objects.exclude(idProd=None).order_by('created_at')

class WeeklyAlertListView(ListView):
    model = AlertProduct
    template_name = 'dispositivos/weekly_alerts.html'
    context_object_name = 'alerts'

    def get_queryset(self):
        one_week_ago = now() - timedelta(days=7)
        return (
            AlertProduct.objects
            .filter(id_alert__created_at__gte=one_week_ago)
            .select_related('id_prod', 'id_alert')
            .order_by('-id_alert__created_at')
        )

class DashboardView(TemplateView):
    template_name = 'dispositivos/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Resumen general
        context['total_devices'] = Device.objects.count()
        context['active_devices'] = Device.objects.filter(estado='ACTIVO').count()
        context['estimated_savings'] = Device.objects.filter(estado='INACTIVO').count() * 15

        # Dispositivos por categoría
        context['devices_by_category'] = Device.objects.values('id_cat__name').annotate(total=Count('id'))

        # Dispositivos por zona
        context['devices_by_zone'] = Device.objects.values('id_zone__name').annotate(total=Count('id'))

        # Alertas de la semana por severidad
        one_week_ago = now() - timedelta(days=7)
        context['alerts_by_severity'] = (
            AlertProduct.objects
            .filter(id_alert__created_at__gte=one_week_ago)
            .values('id_alert__severity')
            .annotate(total=Count('id'))
        )

        # Últimas 10 mediciones
        context['recent_measurements'] = (
            Measurement.objects
            .select_related('idProd')
            .order_by('-created_at')[:10]
        )

        context['recent_alerts'] = (
            AlertProduct.objects
            .filter(id_alert__created_at__gte=one_week_ago)
            .select_related('id_prod', 'id_alert')
            .order_by('-id_alert__created_at')[:5]
        )

        return context

class OrganizationRegisterView(FormView):
    template_name = 'dispositivos/register.html'
    form_class = OrganizationRegisterForm
    success_url = reverse_lazy('login')
