from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action


from .serializer import BankSerializer, DeviceSerializer, DeviceHistorySerializer
from .models import Bank, Device, DeviceHistory



######### Bank CRUD ##########

class AddBank(APIView):
    serializer_class = BankSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ListBanks(APIView):
    def __init__(self):
        return super().__init__()
    
    def get(self, request, *args, **kwargs):
        try:
            banks = Bank.objects.all()
            serializer = BankSerializer(banks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UpdateBank(APIView):
    lookup_field = 'pk'
    def _handle_update(self, request, pk, partial=False):
        instance = get_object_or_404(Bank, pk=pk)
        serializer = BankSerializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True) 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e: 
            return Response({"error": "An unexpected error occurred during update."}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    def patch(self, request, *args, **kwargs):
        return self._handle_update(request, self.kwargs['pk'], partial=True)

    def put(self, request, *args, **kwargs):
        return self._handle_update(request, self.kwargs['pk'], partial=False)
        
class DeleteBank(APIView):
    def __init__(self):
        return super().__init__()
    
    def delete(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(Bank, pk=kwargs['pk'])
            if instance is not None:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    



######### Device CRUD ##########
    
class AddDevice(APIView):
    '''
    This class is for adding a device'''
    serializer_class = DeviceSerializer

    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serial_number = serializer.validated_data['serial_number']
        if Device.objects.filter(serial_number=serial_number).exists():
            return Response({'message':'Device already exist and has been assigned.'}, status=status.HTTP_409_CONFLICT)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ListDevices(APIView):
    def __init__(self):
        return super().__init__()
    

    def get(self, request, *args, **kwargs):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateDevice(APIView):
    allowed_method = ['PATCH', 'PUT']
    def __init__(self):
        return super().__init__()
    
    def patch(self, request, *args, **kwargs):
            try:
                get_instance = get_object_or_404(Device, pk=kwargs['pk'])
                if get_instance is not None:
                    serializer = DeviceSerializer(get_instance, data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
    def put(self, request, *args, **kwargs):
        try:
            get_instance = get_object_or_404(Device, pk=kwargs['pk'])
            if get_instance is not None:
                serializer = DeviceSerializer(get_instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class DeleteDevice(APIView):
    allowed_methods = ['DELETE']
    def __init__(self):
        return super().__init__()
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = get_object_or_404(Device, pk=kwargs['pk'])
            if instance is not None:
                instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)