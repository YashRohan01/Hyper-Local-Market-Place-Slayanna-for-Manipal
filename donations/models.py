from django.db import models
from users.models import User
from products.models import Product

# Create your models here.
class Donation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='donated_products')
    charity_name = models.CharField(max_length=200)
    donation_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.donor.username} donated {self.product.name} to {self.charity_name}"