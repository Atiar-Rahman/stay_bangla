from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from hotels.models import Hotel,Room,HotelImage
from hotels.serializers import HotelSerializer,RoomSerializer,HotelImageSerializer
from hotels.permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

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
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['room_type'] #search name add korte hobe
    ordering_fields = ['price','updated_at'] #for order korer jonno
    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_pk')
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
        # print(hotel_id)
        return HotelImage.objects.filter(hotel_id=hotel_id)
       

    def perform_create(self, serializer):
        hotel = get_object_or_404(Hotel, pk=self.kwargs.get("hotel_pk"))
        print(hotel)
        serializer.save(hotel=hotel)
