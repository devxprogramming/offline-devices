from django.shortcuts import render, redirect, get_list_or_404
from django.views.generic import CreateView, ListView
from django.core.paginator import Paginator

from apps.devices.models import Device, Bank, Branch

def dashboard(request):
    return render(request, 'dashboard.html')


class CreateDeviceView(CreateView):
    template_name = 'DevicesTemplates/createDevice.html'
    queryset = Device.objects.all()
    fields = ['serial_number', 'branch', 'notes']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'createDevice'
        return context
    

class ListDevicesView(ListView):
    template_name = 'DevicesTemplates/listDevices.html'
    queryset = Device.objects.all()
    context_object_name = 'devices'
    paginate_by = 10



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'listDevices'
        return context
