from django.db import models
from auditlog.registry import auditlog


class Bank(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'

        ordering = ["name"]

    def __str__(self):
        return self.name

    
    




class Branch(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="branches")
    branch_name = models.CharField(max_length=255, help_text="Branch Name. \nExample: BANK(ABOKOBI) BRANCH('MADINA', 'ADENTA')")
    about = models.CharField(max_length=255, help_text="You can state the location of that particular branch. \nExample: Kumasi, Accra, etc.", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['bank', 'branch_name'], name='unique_branch')
        ]

        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

        ordering = ["-updated"]

    def __str__(self):
        return self.branch_name
    

class Device(models.Model):
    serial_number = models.CharField(max_length=8, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="devices")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["branch", "serial_number"]),
        ]

    def __str__(self):
        return f"{self.serial_number} - {self.branch}"


models = [
    Bank,
    Branch,
    Device
]

for model in models:
    auditlog.register(model)