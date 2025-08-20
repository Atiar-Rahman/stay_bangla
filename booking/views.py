from rest_framework.viewsets import ModelViewSet
from booking.models import Booking
from booking.serializers import BookingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status as drf_status

class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(room_id=self.kwargs.get('room_pk'))

    def perform_create(self, serializer):
        booking = serializer.save(
            hotel_id=self.kwargs.get('hotel_pk'),
            room_id=self.kwargs.get('room_pk')
        )
        # Mark the room as unavailable
        booking.room.available = False
        booking.room.save()

    @action(detail=True, methods=["post"])
    def confirm_payment(self, request, hotel_pk=None, room_pk=None, pk=None):
        booking = self.get_object()
        if booking.status == "pending":
            booking.status = "confirmed"
            booking.save()
            return Response({"status": "Booking confirmed"})
        return Response({"status": f"Cannot confirm booking with status {booking.status}"}, status=drf_status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get", "post"])
    def cancel_booking(self, request, hotel_pk=None, room_pk=None, pk=None):
            booking = self.get_object()
            if booking.status in ["pending", "confirmed"]:
                # Make room available
                booking.room.available = True
                booking.room.save()
                # Delete the booking
                booking.delete()
                return Response({"status": "Booking cancelled and deleted"})
            return Response({"status": f"Cannot cancel booking with status {booking.status}"}, status=400)
