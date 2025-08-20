from rest_framework.viewsets import ModelViewSet
from hotels.models import Hotel,Room,HotelImage
from hotels.serializers import HotelSerializer,RoomSerializer,HotelImageSerializer

class HotelViewSet(ModelViewSet):
    """
    
    show all user Hotels
    """
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer



class HotelRoomViewSet(ModelViewSet):

    serializer_class = RoomSerializer
    def get_queryset(self):
        return Room.objects.filter(available=True)

class HotelImageViewSet(ModelViewSet):
    queryset = HotelImage.objects.all()
    serializer_class = HotelImageSerializer