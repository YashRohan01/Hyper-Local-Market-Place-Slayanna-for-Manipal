from django.db import models
from users.models import User
from products.models import Product

# Create your models here.
class Transaction(models.Model):
    STATUS_CHOICES = [("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")]

    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="purchases")
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sales")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    transaction_id = models.CharField(max_length=100)  # From payment gateway (e.g., Stripe)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.id}"