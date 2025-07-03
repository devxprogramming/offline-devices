# from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet #, ViewSet
from rest_framework import status
from .serializer import DeviceSerializer, BankSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser


from .serializer import BankSerializer, DeviceSerializer
from .models import Bank, Device
# History models
# from .models import DeviceHistory



# Helper function to handle device history creation





# Bank 

class BankViewSet(ModelViewSet):
    """
    API endpoint with the follow HTTP methods:
    API URL path to banks:
        - `/api/v1/banks/`
        * GET: Lists all the banks.
        * POST: Creates a new bank.
        * PUT: Updates a bank.
        * PATCH: Partially updates a bank.
        * DELETE: Deletes a bank.
    
    """
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    model = Bank
    permission_classes = [AllowAny]

    # Create method
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Read method
    @method_decorator(cache_page(60 * 15, key_prefix="bank_list"))
    def list(self, request, *args, **kwargs):
        model_data = self.model.objects.all()
        serializer = self.get_serializer(model_data, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    # Update method
    def update(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        instance = get_object_or_404(self.model, pk=object_id)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Partial update method
    def partial_update(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        instance = get_object_or_404(self.model, pk=object_id)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # delete method
    def destroy(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        instance = get_object_or_404(self.model, pk=object_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Device

class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    model = Device
    permission_classes = [AllowAny]


    # Create method
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    # Read method
    def list(self, request, *args, **kwargs):
        model_data = self.model.objects.all()
        serializer = self.get_serializer(model_data, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    # Update Method
    def update(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        instance = get_object_or_404(self.model, pk=object_id)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Partial Update
    def partial_update(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        instance = get_object_or_404(self.model, pk=object_id)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    # Delete method
    def destroy(self, request, *args, **kwargs):
        object_id = kwargs['pk']
        instance = get_object_or_404(self.model, pk=object_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




def dashboard(request):
    return render(request, 'dashboard.html')