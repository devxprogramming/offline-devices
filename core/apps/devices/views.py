# from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# from rest_framework import status
from rest_framework.viewsets import ModelViewSet #, ViewSet
from rest_framework import status


from .serializer import BankSerializer, DeviceSerializer
from .models import Bank, Device
# History models
# from .models import DeviceHistory


class BankViewSet(ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance is not None:
                self.perform_destroy(instance)
                return Response({"message": "Bank deleted successfully"},status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (Bank.DoesNotExist, Bank.MultipleObjectsReturned):
            return Response({"error": "Bank not found"}, status.HTTP_404_NOT_FOUND)
        


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer