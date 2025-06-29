import time
from django.db import models
from users.models import User

# Helpers to generate unique file paths using timestamp
def product_main_image_path(instance, filename):
    phone_number = instance.seller.phone_number
    product_title = instance.title.replace(" ", "_")  # Sanitize title
    return f'products_photos/{phone_number}/{product_title}/main_image/{filename}'



def product_additional_image_path(instance, filename):
    phone_number = instance.product.seller.phone_number
    product_title = instance.product.title.replace(" ", "_")  # Sanitize title
    return f'products_photos/{phone_number}/{product_title}/additional_images/{filename}'



# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., textbooks, furniture

    def __str__(self):
        return self.name

# Product model
class Product(models.Model):
    CONDITION_CHOICES = [("new", "New"), ("used", "Used")]
    STATUS_CHOICES = [("available", "Available"), ("sold", "Sold"), ("donated", "Donated")]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="available")
    category = models.ManyToManyField(Category)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    _3d_model_url = models.URLField(blank=True, null=True)
    main_image = models.ImageField(
        upload_to=product_main_image_path,
        verbose_name='Main Product Image'
    )

    def __str__(self):
        return self.title

# Additional product images
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to=product_additional_image_path,
        verbose_name='Product Image'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Image for {self.product.title}"
