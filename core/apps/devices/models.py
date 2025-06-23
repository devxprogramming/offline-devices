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
    serial_number = models.CharField(max_length=255, unique=True)
    status = models.CharField(choices=DEVICE_STATUS, default=DEVICE_STATUS[0][0], max_length=255)
    assigned_to = models.ForeignKey(Bank, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store original values for comparison on save
        self._original_status = self.status
        # If assigned_to is a ForeignKey, store its ID
        self._original_assigned_to_id = self.assigned_to_id 

    def save(self, *args, **kwargs):
        from .models import DeviceHistory # Import locally to avoid circular dependency at module load time

        is_new = self._state.adding
        made_change = False

        # Call the "real" save() method first. This ensures the device instance (especially a new one)
        # has an ID before we try to create a DeviceHistory record linked to it.
        super().save(*args, **kwargs)

        if not is_new:
            if self.status != self._original_status:
                DeviceHistory.objects.create(
                    device=self,
                    status_from=self._original_status,
                    status_to=self.status,
                    reason_for_change="Status updated automatically."
                )
                made_change = True
            
            # Example for tracking assigned_to changes (optional for now, but good to consider)
            # if self.assigned_to_id != self._original_assigned_to_id:
            #     # Logic to get bank names if needed for reason_for_change
            #     DeviceHistory.objects.create(
            #         device=self,
            #         status_from=self._original_status, # Or a special status like 'REASSIGNED'
            #         status_to=self.status, # Or new status 'REASSIGNED'
            #         reason_for_change=f"Device assignment changed."
            #     )
            #     made_change = True

        # Update original values after potential history creation and successful save
        if made_change or is_new: # Update if a change was made or if it's a new instance
            self._original_status = self.status
            self._original_assigned_to_id = self.assigned_to_id

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
