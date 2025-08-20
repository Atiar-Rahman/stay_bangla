from rest_framework_nested import routers
from hotels.views import HotelViewSet,HotelRoomViewSet
from django.urls import path,include
router = routers.DefaultRouter()
router.register('hotels',HotelViewSet)

room_router = routers.NestedSimpleRouter(router,'hotels',lookup='room')
room_router.register('rooms',HotelRoomViewSet,basename='hotel-room')



urlpatterns = [
    path("",include(router.urls)),
    path("",include(room_router.urls))
]
