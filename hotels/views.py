from rest_framework.viewsets import ModelViewSet
from hotels.models import Hotel,Room
from hotels.serializers import HotelSerializer,RoomSerializer

class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer



class HotelRoomViewSet(ModelViewSet):
    queryset = Room.objects.all()

    serializer_class = RoomSerializer