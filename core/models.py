
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class PlatformApiCall(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    requested_url = models.CharField(max_length=1024)
    requested_data = models.JSONField(null=True, blank=True)
    response_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.requested_url} by {self.user}"
