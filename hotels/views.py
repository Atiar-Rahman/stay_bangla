from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from hotels.models import Hotel, Room, HotelImage
from .serializers import HotelSerializer, RoomSerializer, HotelImageSerializer


# Custom Permission: Admins can write, others can only read
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Anyone can GET
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only staff (admin) can POST/PUT/PATCH/DELETE
        return request.user and request.user.is_staff


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_pk')  # Nested lookup
        return Room.objects.filter(hotel_id=hotel_id)
    
    def perform_create(self, serializer):
        # Assign room to the correct hotel automatically
        hotel_id = self.kwargs.get('hotel_pk')
        serializer.save(hotel_id=hotel_id)


class HotelImageViewSet(viewsets.ModelViewSet):
    serializer_class = HotelImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        # Nested router passes hotel_pk in kwargs
        hotel_id = self.kwargs.get('hotel_pk')
        return HotelImage.objects.filter(hotel_id=hotel_id)

    def perform_create(self, serializer):
        # Automatically assign image to the correct hotel
        hotel_id = self.kwargs.get('hotel_pk')
        serializer.save(hotel_id=hotel_id)
