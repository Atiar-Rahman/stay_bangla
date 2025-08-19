from rest_framework import viewsets
from rest_framework.response import Response
from hotels.models import Hotel, Room, HotelImage
from .serializers import HotelSerializer, RoomSerializer, HotelImageSerializer

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_pk')  # Nested lookup
        return Room.objects.filter(hotel_id=hotel_id)
    
    def perform_create(self, serializer):
        # Assign room to the correct hotel automatically
        hotel_id = self.kwargs.get('hotel_pk')
        serializer.save(hotel_id=hotel_id)

class HotelImageViewSet(viewsets.ModelViewSet):
    serializer_class = HotelImageSerializer

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_pk')  # Nested lookup
        return HotelImage.objects.filter(hotel_id=hotel_id)

