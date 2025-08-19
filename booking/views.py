from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from .models import Booking
from .serializers import BookingSerializer
from hotels.models import Hotel, Room


class BookingViewSet(viewsets.ModelViewSet):
    """
    - Users: CRUD only their own bookings, only if pending
    - Admin: Full access + approve/reject actions
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        hotel_id = self.kwargs.get("hotel_id")
        room_id = self.kwargs.get("room_id")

        if user.is_staff:  # admin sees all bookings
            qs = Booking.objects.all()
        else:  # user sees only their own bookings
            qs = Booking.objects.filter(user=user)

        if hotel_id:
            qs = qs.filter(hotel_id=hotel_id)

        if room_id:
            qs = qs.filter(room_id=room_id)

        return qs

    def perform_create(self, serializer):
        """
        Save booking with user + hotel + room.
        Booking always starts as 'pending'.
        """
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

        serializer.save(user=self.request.user, hotel=hotel, room=room, status="pending")

    def perform_update(self, serializer):
        """
        Users: can update only if pending.
        Admin: can update anytime.
        """
        booking = self.get_object()
        if not self.request.user.is_staff and booking.status != "pending":
            raise PermissionDenied("You cannot update this booking after approval.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Users: can delete only if pending.
        Admin: can delete anytime.
        """
        if not self.request.user.is_staff and instance.status != "pending":
            raise PermissionDenied("You cannot cancel this booking after approval.")
        instance.delete()

    #  Custom actions for Admin
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        booking = self.get_object()
        booking.status = "confirmed"
        booking.save()
        return Response({"status": "Booking approved"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        booking = self.get_object()
        booking.status = "cancelled"
        booking.save()
        return Response({"status": "Booking rejected"}, status=status.HTTP_200_OK)
