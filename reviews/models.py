from django.db import models
from users.models import User


# Create your models here.
class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1-5 stars

    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_given")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("reviewer", "seller")  # Prevent duplicate reviews

    def __str__(self):
        return f"{self.rating}★ review for {self.seller}"