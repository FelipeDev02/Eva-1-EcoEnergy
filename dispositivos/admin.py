from django.contrib import admin
from .models import Organization, Zone, Category, Product, Device, Measurement, Alert, AlertProduct

admin.site.register(Organization)
admin.site.register(Zone)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Device)
admin.site.register(Measurement)
admin.site.register(Alert)
admin.site.register(AlertProduct)