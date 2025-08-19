from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id", "user", "hotel", "room",
            "check_in", "check_out", "guests",
            "is_confirmed", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
