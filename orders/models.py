
from django.db import models
from core.models import Product, Customer, Seller, TimestampedModel
from django.conf import settings
from decimal import Decimal

class Order(TimestampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItem')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def recalc_amount(self):
        total = sum([oi.subtotal for oi in self.items.all()])
        self.amount = total
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.unit_price = self.unit_price or self.product.amount
        self.subtotal = Decimal(self.quantity) * Decimal(self.unit_price)
        super().save(*args, **kwargs)
