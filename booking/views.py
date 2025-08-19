from rest_framework import viewsets, permissions
from .models import Booking
from .serializers import BookingSerializer
from hotels.models import Hotel, Room
from rest_framework.exceptions import NotFound

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_id")
        room_id = self.kwargs.get("room_id")

        qs = Booking.objects.filter(user=self.request.user)

        if hotel_id:
            qs = qs.filter(hotel_id=hotel_id)

        if room_id:
            qs = qs.filter(room_id=room_id)

        return qs

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get("hotel_id")
        room_id = self.kwargs.get("room_id")

        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            raise NotFound("Hotel not found")

        try:
            room = Room.objects.get(id=room_id, hotel=hotel)
        except Room.DoesNotExist:
            raise NotFound("Room not found in this hotel")

        serializer.save(user=self.request.user, hotel=hotel, room=room)
