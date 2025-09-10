from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email", read_only=True)
    hotel_name = serializers.CharField(source="hotel.name", read_only=True)
    

    class Meta:
        model = Review
        fields = [
            "id",
            "user_email",
            "hotel_name",
            "rating",
            "title",
            "comment",
            "is_approved",
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["id", "user_email", "hotel_name", "is_approved", "created_at", "updated_at"]
