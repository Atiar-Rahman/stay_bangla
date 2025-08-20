from django.db import models
from users.models import User
from hotels.models import Hotel,Room
import uuid

# Create your models here.
# booking/models.py

class Booking(models.Model):
    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("pending", "Pending"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    booking_reference = models.CharField(max_length=100, unique=True, blank=True)  # allow blank initially
    created_at = models.DateTimeField(auto_now_add=True)
    cancellation_allowed = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = f"REF-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_reference} by {self.user.email}"
