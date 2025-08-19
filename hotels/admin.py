from django.contrib import admin
from hotels.models import Hotel,HotelImage,Room
# Register your models here.

admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(Room)