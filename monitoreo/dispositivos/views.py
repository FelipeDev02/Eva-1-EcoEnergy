from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Device

class DeviceListView(ListView):
    model = Device
    template_name = 'dispositivos/device_list.html'
    context_object_name = 'devices'

class DeviceDetailView(DetailView):
    model = Device
    template_name = 'dispositivos/device_detail.html'
    context_object_name = 'device'


# Create your views here.
