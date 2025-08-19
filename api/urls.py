from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from hotels.views import HotelViewSet, RoomViewSet, HotelImageViewSet

# Main router
router = DefaultRouter()
router.register(r'hotels', HotelViewSet, basename='hotel')

# Nested router for rooms under hotels
hotels_router = NestedDefaultRouter(router, r'hotels', lookup='hotel')
hotels_router.register(r'rooms', RoomViewSet, basename='hotel-rooms')
hotels_router.register(r'images', HotelImageViewSet, basename='hotel-images')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(hotels_router.urls)),
]
