from rest_framework.viewsets import ModelViewSet
from hotels.models import Hotel,Room,HotelImage
from hotels.serializers import HotelSerializer,RoomSerializer,HotelImageSerializer
from hotels.permissions import IsAdminOrReadOnly

class HotelViewSet(ModelViewSet):
    """
    show all user Hotels
    """
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAdminOrReadOnly]


class HotelRoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_pk']
        return Room.objects.filter(hotel_id=hotel_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['hotel_id'] = self.kwargs.get('hotel_pk')
        return context

    def perform_create(self, serializer):
        # Automatically assign hotel based on URL
        hotel_id = self.kwargs['hotel_pk']
        room = serializer.save(hotel_id=hotel_id)
        # Initialize available_rooms and is_available
        room.available_rooms = room.total_rooms
        room.is_available = room.available_rooms > 0
        room.save()

class HotelImageViewSet(ModelViewSet):
    serializer_class = HotelImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_pk")   # nested router থেকে আসবে
        return HotelImage.objects.filter(hotel_id=hotel_id)

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get("hotel_pk")
        serializer.save(hotel_id=hotel_id)   
