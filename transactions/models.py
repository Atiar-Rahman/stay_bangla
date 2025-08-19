from django.db import models
from users.models import User
from booking.models import Booking
# Create your models here.
class Transaction(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.id} - {self.user.email}"