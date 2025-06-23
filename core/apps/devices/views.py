# from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# from rest_framework import status
from rest_framework.viewsets import ModelViewSet #, ViewSet
from rest_framework import status
from .serializer import DeviceHistorySerializer, DeviceSerializer, BankSerializer


from .serializer import BankSerializer, DeviceSerializer
from .models import Bank, Device, DeviceHistory
# History models
# from .models import DeviceHistory



# Helper function to handle device history creation
def save_device_history(device, status_from, status_to, reason_for_change):
    DeviceHistory.objects.create(
        device=device,
        status_from=status_from,
        status_to=status_to,
        reason_for_change=reason_for_change
    )

class BankViewSet(ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bank = serializer.save()
        # Saving the new bank instance to device history
        
        return Response(
            {"message": "Bank created successfully", "bank": BankSerializer(bank).data},
            status=status.HTTP_201_CREATED
        )


    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(Bank, pk=kwargs.get('pk'))
            if instance is not None:
                self.perform_destroy(instance)
                return Response({"message": "Bank deleted successfully"},status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except (Bank.DoesNotExist, Bank.MultipleObjectsReturned):
            return Response({"error": "Bank not found"}, status.HTTP_404_NOT_FOUND)
        


class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer



# Device History ViewSet

class DeviceHistoryViewSet(ModelViewSet):
    """
    ViewSet for Device History.
    """

    queryset = DeviceHistory.objects.all()
    serializer_class = DeviceHistorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device_history = serializer.save()
        return Response(
            {"message": "Device history created successfully", "device_history": DeviceHistorySerializer(device_history).data},
            status=status.HTTP_201_CREATED
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(DeviceHistory, pk=kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(DeviceHistory, pk=kwargs.get('pk'))
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        device_history = serializer.save()
        return Response(
            {"message": "Device history updated successfully", "device_history": DeviceHistorySerializer(device_history).data},
            status=status.HTTP_200_OK
        )
    
    def partial_update(self, request, *args, **kwargs):
        instance = get_object_or_404(DeviceHistory, pk=kwargs.get('pk'))
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        device_history = serializer.save()
        return Response(
            {"message": "Device history partially updated successfully", "device_history": DeviceHistorySerializer(device_history).data},
            status=status.HTTP_200_OK
        )


