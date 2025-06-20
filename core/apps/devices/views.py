# from django.http import HttpResponse, JsonResponse
# from rest_framework.response import Response
# from rest_framework import status
from rest_framework.viewsets import ModelViewSet #, ViewSet



from .serializer import BankSerializer, DeviceSerializer
from .models import Bank, Device
# History models
# from .models import DeviceHistory


class BankViewSet(ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer