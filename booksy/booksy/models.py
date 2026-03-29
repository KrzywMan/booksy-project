from django.db import models
from django.contrib.auth.models import User

class Hardware(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Repair', 'Repair'),
    ]

    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True, null=True)
    purchase_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    assigned_to = models.EmailField(blank=True, null=True) # Zgodnie z formatem j.doe@booksy.com
    notes = models.TextField(blank=True, null=True)
    history = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.name} ({self.status})"