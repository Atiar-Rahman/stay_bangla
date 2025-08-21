# booking/models.py
from django.db import models
from users.models import User
from hotels.models import Room, Hotel

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.PositiveIntegerField(default=1)
    num_rooms = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    booking_reference = models.CharField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cancellation_allowed = models.BooleanField(default=True)

    def __str__(self):
        return f"Booking {self.booking_reference} by {self.user.email}"
