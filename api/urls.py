from rest_framework_nested import routers
from hotels.views import HotelViewSet, HotelRoomViewSet, HotelImageViewSet
from booking.views import BookingViewSet
from django.urls import path, include

# Main router
router = routers.DefaultRouter()
router.register('hotels', HotelViewSet)

# Nested router for rooms under hotels
room_router = routers.NestedSimpleRouter(router, 'hotels', lookup='hotel')
room_router.register('rooms', HotelRoomViewSet, basename='hotel-room')

# Nested router for bookings under rooms (room-level booking)
booking_router = routers.NestedSimpleRouter(room_router, 'rooms', lookup='room')
booking_router.register('bookings', BookingViewSet, basename='room-booking')

# Nested router for images under rooms
image_router = routers.NestedSimpleRouter(room_router, 'rooms', lookup='room')
image_router.register('images', HotelImageViewSet, basename='room-image')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(room_router.urls)),
    path("", include(booking_router.urls)),
    path("", include(image_router.urls)),
]
