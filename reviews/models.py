from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from hotels.models import Hotel

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "hotel"]

    def __str__(self):
        return f"{self.hotel.name} Review by {self.user.email}"
