from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('OWNER', 'Owner'),
        ('STAFF', 'Sales/Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STAFF')

    def __str__(self):
        return f"{self.username} ({self.role})"

class Inventory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('SALE', 'Sale'),
        ('PURCHASE', 'Purchase'),
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name if self.product else 'Deleted'} ({self.transaction_date})"

class Schedule(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    google_event_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
