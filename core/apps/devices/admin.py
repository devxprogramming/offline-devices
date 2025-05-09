from django.contrib import admin
from .models import Device, DeviceHistory, Bank



admin.site.register(Bank)
admin.site.register(DeviceHistory)


class DeviceAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'status', 'assigned_to']

admin.site.register(Device, DeviceAdmin)