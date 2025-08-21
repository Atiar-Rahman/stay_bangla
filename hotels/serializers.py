from rest_framework import serializers
from hotels.models import Hotel, HotelImage, Room

class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ["id", "hotel", "image", "caption", "is_featured", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]



from rest_framework import serializers
from hotels.models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id", "room_type", "price_per_night",
            "capacity", "total_rooms", "available_rooms", "is_available"
        ]
        read_only_fields = ["id", "available_rooms", "is_available"]

    def validate(self, data):
        hotel_id = self.context.get('hotel_id')
        room_type = data.get("room_type")

        # Prevent duplicate room types per hotel
        if Room.objects.filter(hotel_id=hotel_id, room_type=room_type).exists():
            raise serializers.ValidationError(
                f"A room with type '{room_type}' already exists for this hotel."
            )

        return data

    def create(self, validated_data):
        # Automatically set hotel from context
        hotel_id = self.context.get('hotel_id')
        validated_data['hotel_id'] = hotel_id
        return super().create(validated_data)


class HotelSerializer(serializers.ModelSerializer):
    images = HotelImageSerializer(many=True, read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    amenities = serializers.CharField(required=False, allow_blank=True)

    def to_representation(self, instance):
        """Return amenities as a list in API response."""
        ret = super().to_representation(instance)
        ret['amenities'] = instance.get_amenities_list()
        return ret

    def validate_amenities(self, value):
        """Clean up the input string."""
        if isinstance(value, str):
            # Remove extra spaces
            value = ','.join([x.strip() for x in value.split(',')])
        return value

    class Meta:
        model = Hotel
        fields = [
            "id", "name", "slug", "address", "city", "description",
            "amenities", "contact_email", "contact_phone",
            "images", "rooms"
        ]
        read_only_fields = ["id", "slug", "images", "rooms"]
