from django.http import HttpResponseRedirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking
from hotels.models import Hotel
from .serializers import BookingSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAdminUser
from sslcommerz_lib import SSLCOMMERZ 
from rest_framework.decorators import api_view
import random
from django.conf import settings as main_settings
from rest_framework import status


class HotelBookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_pk")
        room_id = self.kwargs.get("room_pk")
        queryset = Booking.objects.all()
        if hotel_id:
            queryset = queryset.filter(hotel_id=hotel_id)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        hotel_id = self.kwargs.get("hotel_pk")
        
        # Only try to fetch hotel if hotel_id exists
        if hotel_id:
            try:
                context["hotel"] = Hotel.objects.get(id=hotel_id)
            except Hotel.DoesNotExist:
                context["hotel"] = None
        else:
            context["hotel"] = None
        
        context["user"] = self.request.user
        return context


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=True, methods=["get","post"], url_path="cancel")
    def cancel_booking(self, request, hotel_pk=None, room_pk=None, pk=None):
        booking = self.get_object()
        if booking.status == "cancelled":
            return Response({"detail": "Booking already cancelled."}, status=400)

        # Cancel booking
        booking.status = "cancelled"
        booking.save()

        # Update room availability
        room = booking.room
        if room:
            room.available_rooms += booking.num_rooms
            room.available_rooms = min(room.available_rooms, room.total_rooms)
            room.is_available = room.available_rooms > 0
            room.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=200)


class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Swagger / fake view support
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()

        # Return empty if user is not authenticated
        if not self.request.user.is_authenticated:
            return Booking.objects.none()

        # User can see only their own bookings
        return Booking.objects.filter(user=self.request.user)


    def get_serializer_context(self):
        context = super().get_serializer_context()
        hotel_id = self.kwargs.get("hotel_pk")
        if hotel_id:
            context["hotel"] = Hotel.objects.get(id=hotel_id)
        context["user"] = self.request.user
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_booking(self, request, pk=None, *args, **kwargs):
        booking = self.get_object()
        if booking.status == "cancelled":
            return Response({"detail": "Booking already cancelled."}, status=400)

        # Only allow cancel if user owns it
        if booking.user != request.user:
            return Response({"detail": "Not allowed."}, status=403)

        # Cancel booking
        booking.status = "cancelled"
        booking.save()

        # Restore room availability
        room = booking.room
        if room:
            room.available_rooms += booking.num_rooms
            room.is_available = room.available_rooms > 0
            room.save()

        return Response(self.get_serializer(booking).data, status=200)


# -------------------- Admin Booking ViewSet --------------------
class BookingAdminViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Admin can see ALL bookings
        return Booking.objects.all()

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel_booking(self, request, pk=None, *args, **kwargs):
        booking = self.get_object()
        if booking.status == "cancelled":
            return Response({"detail": "Booking already cancelled."}, status=400)

        # Admin can always cancel
        booking.status = "cancelled"
        booking.save()

        # Restore room availability
        room = booking.room
        if room:
            room.available_rooms += booking.num_rooms
            room.is_available = room.available_rooms > 0
            room.save()

        return Response(self.get_serializer(booking).data, status=200)
    
    


# payment all views

@api_view(['POST'])
def initiate_payment(request):
    
    # collect data
    user = request.user
    amount = request.data.get("amount")
    num_rooms = request.data.get("num_rooms")
    booking_id = request.data.get('booking_id')
    # print(user)
    # print(amount)
    # print(num_rooms)
    tran_id = str(random.randint(10**9, 10**10 - 1))
    settings = { 'store_id': 'phima67ddc8dba290b', 'store_pass': 'phima67ddc8dba290b@ssl', 'issandbox': True }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f'txn_{tran_id}_{booking_id}'
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/fail/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/v1/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f'{user.first_name} {user.last_name}'
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = num_rooms
    post_body['product_name'] = "Hotel Room booking"
    post_body['product_category'] = "restrudant"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) # API response
    print(response)
    # Need to redirect user to response['GatewayPageURL']
    if response.get("status") == 'SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)


# Payment success
@api_view(['POST'])
def payment_success(request):
    tran_id = request.data.get("tran_id")  # txn_<random>_<booking_id>
    booking_id = tran_id.split("_")[-1]
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = "confirmed"
        booking.save()
    except Booking.DoesNotExist:
        pass  # optionally log

    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/showbooking/")

# Payment cancel
@api_view(['POST'])
def payment_cancel(request):
    tran_id = request.data.get("tran_id")
    booking_id = tran_id.split("_")[-1]
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = "pending"
        booking.save()
    except Booking.DoesNotExist:
        pass

    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/showbooking/")

# Payment fail
@api_view(['POST'])
def payment_fail(request):
    tran_id = request.data.get("tran_id")
    booking_id = tran_id.split("_")[-1]
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = "failed"
        booking.save()
    except Booking.DoesNotExist:
        pass

    return HttpResponseRedirect(f"{main_settings.FRONTEND_URL}/dashboard/showbooking/")