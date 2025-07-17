from django.contrib import admin
from django.db import models
from django import forms

# Main models tables
from .models import Device, Bank, Branch

# admin.site.register(Branch)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"rows": 4, "cols": 50})
        },
    }



class DeviceInlineTable(admin.TabularInline):
    model = Device
    extra = 0
    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(attrs={"rows": 2, "cols": 60})
        },
    }

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    # inlines = [DeviceInlineTable]
    list_display = ('branch_name', 'bank')



admin.site.register(Bank)