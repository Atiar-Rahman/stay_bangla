from rest_framework.viewsets import ModelViewSet
from booking.models import Booking
from booking.serializers import BookingSerializer


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer