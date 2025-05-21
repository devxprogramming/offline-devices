from .models import Bank, Device, DeviceHistory
from rest_framework import serializers


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ('id', 'name', 'created', 'updated')


class DeviceSerializer(serializers.ModelSerializer):
    serial_number = serializers.CharField(max_length=255, help_text="Serial Number should be of length 7. \nExample: 1013435")
    class Meta:
        model = Device
        fields = ('id', 'serial_number', 'status', 'assigned_to', 'created', 'updated') 


    def validate(self, attrs):
        if 'serial_number' in attrs and len(attrs['serial_number']) != 7:
            raise serializers.ValidationError("Serial Number should be of length 7. \nExample: 1013435")
        return attrs
        


class DeviceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceHistory
        fields = ('id', 'device', 'status_from', 'status_to', 'changed_at', 'reason_for_change')