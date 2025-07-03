from .models import Bank, Device, Branch
from rest_framework import serializers


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    bank = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Branch
        fields = "__all__"

class DeviceSerializer(serializers.ModelSerializer):
    serial_number = serializers.CharField(max_length=255, help_text="Serial Number should be of length 7. \nExample: 1013435")
    class Meta:
        model = Device
        fields = "__all__"
        
