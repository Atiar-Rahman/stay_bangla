from rest_framework import serializers
from hotels.models import Hotel,HotelImage,Room


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ["id", "hotel", "image", "caption", "is_featured", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]



class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "hotel", "room_type", "price", "capacity", "available"]
        read_only_fields = ["id"]


class HotelSerializer(serializers.ModelSerializer):
    images = HotelImageSerializer(source="hotelimage_set", many=True, read_only=True)
    rooms = RoomSerializer(source="room_set", many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = [
            "id", "name", "slug", "address", "city", "description",
            "stars", "price_per_night", "amenities", "contact_email",
            "contact_phone", "available_rooms", "images", "rooms"
        ]
        read_only_fields = ["id", "slug", "images", "rooms"]