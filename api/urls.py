from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from hotels.views import HotelViewSet, RoomViewSet, HotelImageViewSet
from booking.views import BookingViewSet

# Main router
router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotel')

# Nested router for rooms and images under hotels
hotels_router = NestedDefaultRouter(router, r'hotels', lookup='hotel')
hotels_router.register(r'rooms', RoomViewSet, basename='hotel-rooms')
hotels_router.register(r'images', HotelImageViewSet, basename='hotel-images')
hotels_router.register(r'bookings', BookingViewSet, basename='hotel-bookings')

# Nested router for bookings under specific rooms
rooms_router = NestedDefaultRouter(hotels_router, r'rooms', lookup='room')
rooms_router.register(r'bookings', BookingViewSet, basename='room-bookings')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(hotels_router.urls)),
    path('', include(rooms_router.urls)),
]
