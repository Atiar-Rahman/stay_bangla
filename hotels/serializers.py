from rest_framework import serializers
from django.shortcuts import get_object_or_404
from hotels.models import Hotel, HotelImage, Room


class HotelImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = HotelImage
        fields = [
            "id",
            "image",     
        ]
        



class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id", "room_type", "price_per_night",
            "capacity", "total_rooms", "available_rooms", "is_available"
        ]
        read_only_fields = ["id", "available_rooms", "is_available"]

    def validate(self, data):
        hotel_id = self.context.get("hotel_id")
        if not hotel_id:
            raise serializers.ValidationError("Hotel ID is required to validate room data.")

        room_type = data.get("room_type")

        # Prevent duplicate room types per hotel
        if Room.objects.filter(hotel_id=hotel_id, room_type=room_type).exists():
            raise serializers.ValidationError(
                f"A room with type '{room_type}' already exists for this hotel."
            )
        return data

    def create(self, validated_data):
        hotel_id = self.context.get("hotel_id")
        if not hotel_id:
            raise serializers.ValidationError("Hotel ID is required to create a room.")

        # Assign actual hotel object, not just the ID
        validated_data["hotel"] = get_object_or_404(Hotel, pk=hotel_id)
        return super().create(validated_data)


class HotelSerializer(serializers.ModelSerializer):
    images = HotelImageSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    amenities = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Hotel
        fields = [
            "id", "name", "slug", "address", "city", "description",
            "amenities", "contact_email", "contact_phone",
            "images", "rooms"
        ]
        read_only_fields = ["id", "slug", "images", "rooms"]

    def to_representation(self, instance):
        """Return amenities as a list in API response."""
        ret = super().to_representation(instance)
        if hasattr(instance, "get_amenities_list"):
            ret["amenities"] = instance.get_amenities_list()
        return ret

    def validate_amenities(self, value):
        """Clean up the input string before saving."""
        if isinstance(value, str):
            value = ",".join([x.strip() for x in value.split(",") if x.strip()])
        return value
