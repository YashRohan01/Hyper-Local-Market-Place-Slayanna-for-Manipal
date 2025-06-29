from django.db import models
from users.models import User
from products.models import Product,Category


# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    notified = models.BooleanField(default=False)  # True if user is alerted about a match

    def __str__(self):
        return f"{self.user}'s wishlist item"