from django.db import models
from products.models import Product

# Create your models here.
class PricingSuggestion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pricing_suggestions")
    suggested_price = models.DecimalField(max_digits=10, decimal_places=2)
    algorithm_version = models.CharField(max_length=50)  # e.g., "PyTorch v1.0"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggested ₹{self.suggested_price} for {self.product}"