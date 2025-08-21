from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking
from hotels.models import Hotel
from .serializers import BookingSerializer

class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_pk")
        room_id = self.kwargs.get("room_pk")
        queryset = Booking.objects.all()
        if hotel_id:
            queryset = queryset.filter(hotel_id=hotel_id)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        hotel_id = self.kwargs.get("hotel_pk")
        context["hotel"] = Hotel.objects.get(id=hotel_id)
        context["user"] = self.request.user
        return context

    def perform_create(self, serializer):
        serializer.save()


    @action(detail=True, methods=["get","post"], url_path="cancel")
    def cancel_booking(self, request, hotel_pk=None, room_pk=None, pk=None):
        booking = self.get_object()
        if booking.status == "cancelled":
            return Response({"detail": "Booking already cancelled."}, status=400)

        # Cancel booking
        booking.status = "cancelled"
        booking.save()

        # Update room availability
        room = booking.room
        if room:
            room.available_rooms += booking.num_rooms
            room.available_rooms = min(room.available_rooms, room.total_rooms)
            room.is_available = room.available_rooms > 0
            room.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=200)
