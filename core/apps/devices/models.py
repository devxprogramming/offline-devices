from django.db import models

class Bank(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

DEVICE_STATUS = (
    ('NEW_AVAILABLE', 'New - Available for Assignment'),
    ('ASSIGNED', 'Assigned to Bank'),
    ('RETURNED_FAULTY', 'Returned - Faulty'),
    ('RETURNED_UPGRADE', 'Returned - Needs Upgrade'),
    ('IN_CUSTODY', 'In Custody (Porcessing)'),
    ('DISPATCHED', 'Dispatched (Sent back to Bank)'),
)


class Device(models.Model):
    serial_number = models.CharField(max_length=255)
    status = models.CharField(choices=DEVICE_STATUS, default=DEVICE_STATUS, max_length=255)
    assigned_to = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.serial_number} {self.status}"
    
    class Meta:
        ordering = ['-updated']
    

class DeviceHistory(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    status_from = models.CharField(choices=DEVICE_STATUS, max_length=255)
    status_to = models.CharField(choices=DEVICE_STATUS, max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)
    reason_for_change = models.TextField(blank=True, null=True, help_text="e.g., 'Software upgrade v2.1 required', 'Screen malfunction reported by Ecom Bank Branch X'")

    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = 'Device History'



# https://pypi.org/project/selenium-base/