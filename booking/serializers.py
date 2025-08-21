from rest_framework.serializers import ModelSerializer
from booking.models import Booking

class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ['check_in','check_out']