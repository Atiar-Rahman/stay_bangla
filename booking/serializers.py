from rest_framework import serializers
from .models import Booking
from hotels.models import Room
import uuid

class BookingSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)
    room_name = serializers.CharField(source="room.room_type", read_only=True)
    room_type = serializers.CharField(write_only=True)  # user provides desired room type

    check_in = serializers.DateField(required=True)
    check_out = serializers.DateField(required=True)
    num_guests = serializers.IntegerField(required=True, min_value=1)
    num_rooms = serializers.IntegerField(required=True, min_value=1)

    class Meta:
        model = Booking
        fields = [
            "id", "user_email", "hotel_name", "room_name",
            "room", "room_type",
            "check_in", "check_out", "num_guests", "num_rooms",
            "amount", "status", "booking_reference", "cancellation_allowed", "created_at"
        ]
        read_only_fields = [
            "id", "user_email", "hotel_name", "room_name", "room",
            "amount", "booking_reference", "created_at", "status", "cancellation_allowed"
        ]

    def create(self, validated_data):
        # Extract room_type from validated_data
        room_type = validated_data.pop("room_type")

        # Get hotel from context (provided in view's perform_create)
        hotel = self.context.get("hotel")
        if not hotel:
            raise serializers.ValidationError({"hotel": "Hotel context is required."})

        user = self.context["request"].user
        num_rooms = validated_data["num_rooms"]
        check_in = validated_data["check_in"]
        check_out = validated_data["check_out"]

        # Validate dates
        nights = (check_out - check_in).days
        if nights <= 0:
            raise serializers.ValidationError({
                "check_out": "Check-out date must be after check-in date."
            })

        # Auto-select first available room of requested type
        room = Room.objects.filter(
            hotel=hotel,
            room_type=room_type,
            is_available=True,
            available_rooms__gte=num_rooms
        ).first()
        if not room:
            raise serializers.ValidationError(
                f"No available {room_type} rooms in this hotel."
            )

        # Calculate amount
        amount = room.price_per_night * nights * num_rooms
        booking_reference = f"REF-{uuid.uuid4().hex[:10].upper()}"

        # Create booking
        booking = Booking.objects.create(
            user=user,
            hotel=hotel,
            room=room,
            amount=amount,
            booking_reference=booking_reference,
            status="pending",
            **validated_data
        )

        # Update room availability
        room.available_rooms -= num_rooms
        room.is_available = room.available_rooms > 0
        room.save()

        return booking
