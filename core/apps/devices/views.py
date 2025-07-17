# from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet #, ViewSet
from .serializer import DeviceSerializer, BankSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .serializer import BranchSerializer
from .models import Bank, Device, Branch
# History models
# from .models import DeviceHistory

from .pagination import DevicePagination



# Helper function to handle device history creation
from services.exportor import export_branch_devices




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
    @method_decorator(cache_page(60 * 15, key_prefix="bank_list")) # cache for 15 minutes
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
    pagination_class = DevicePagination


    # Create method
    def create(self, request, *args, **kwargs):
        serial = request.data.get('serial_number')
        # Early‐out if it’s already in DB
        if Device.objects.filter(serial_number=serial).exists():
            return Response(
                {"error": "Device already exists."},
                status=status.HTTP_409_CONFLICT
            )

        # Otherwise proceed normally
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # Read method
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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


class BranchViewSet(ModelViewSet):
    """
    API endpoint for managing Branches.
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = super().get_queryset()

        bank_id = self.request.query_params.get('bank_id')
        if bank_id:
            try:
                data = {}
                bank = Bank.objects.get(pk=bank_id)
                branches = bank.branches.all()
                
                # Build branches list
                branch_names = (
                    [b.branch_name for b in branches]
                    if len(branches) > 1
                    else ['No branches found']
                )
                data['bank'] = bank.name
                data['branches'] = branch_names

                serializer = self.get_serializer(branches, many=True)
                specificBranches = [b['branch_name'] for b in serializer.data]
                return Response(
                    {"bank": bank.name, "branches": serializer.data}, 
                status.HTTP_200_OK)
            except Bank.DoesNotExist:
                return Response({"error":"Bank does not exits"})
            except Bank.MultipleObjectsReturned:
                return Response({"error": "got more than one bank"})
            except Exception as e:
                return Response(f"[Error] occured when fetching branches. \n Error Log: {e}", status.HTTP_404_NOT_FOUND)
        else:
            return Response(self.get_serializer(self.queryset, many=True), status.HTTP_200_OK)

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     bank_id = self.request.query_params.get('bank_id')
    #     return qs.filter(bank_id=bank_id).all() if bank_id else qs

    @action(detail=True, methods=['get'], url_path='export-devices')
    def export_devices(self, request, pk=None):
        if pk is not None:
            export_format = request.query_params.get("format", "csv")
            return export_branch_devices(branch_id=pk, export_format='csv')
        return Response({"error": "Branch not found"}, status.HTTP_404_NOT_FOUND)