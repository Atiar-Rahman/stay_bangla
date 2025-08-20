from rest_framework import serializers
from django.db.models import Q
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id", "user", "hotel", "room",
            "check_in", "check_out", "num_guests",
            "amount", "booking_reference",
            "created_at", "status"
        ]
        read_only_fields = ["id", "user", "created_at", "booking_reference", "cancellation_allowed", "status"]

    def validate(self, data):
        room = data.get("room")
        check_in = data.get("check_in")
        check_out = data.get("check_out")

        if room and check_in and check_out:
            overlapping = Booking.objects.filter(
                room=room,
                status__in=["confirmed","pending"]
            ).filter(
                Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
            )
            if overlapping.exists():
                raise serializers.ValidationError(
                    "This room is already booked for the selected dates."
                )

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        # New bookings start as pending
        validated_data['status'] = "pending"
        return super().create(validated_data)
