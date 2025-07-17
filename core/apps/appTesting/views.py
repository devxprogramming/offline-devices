from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, TemplateView

from rest_framework.response import Response
from rest_framework import status

from apps.devices.models import Device

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
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            serial_number = request.POST.get('serial_number')
            branch = request.POST.get('branch')
            notes = request.POST.get('notes')
            device = Device.objects.create(serial_number=serial_number, branch=branch, notes=notes)
            if Device.objects.filter(serial_number=serial_number).exists():
                return Response({'error': 'Device with this serial number already exists.'}, status.HTTP_400_BAD_REQUEST)
            return redirect('listDevices')
    

class ListDevicesView(ListView):
    template_name = 'DevicesTemplates/listDevices.html'
    queryset = Device.objects.all()
    context_object_name = 'devices'
    paginate_by = 10



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'listDevices'
        return context


class BranchBaseExport(TemplateView):
    template_name = 'DevicesTemplates/branchBasedExport.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = "branch-based-export"
        return context
    