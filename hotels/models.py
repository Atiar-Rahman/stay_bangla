from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    description = models.TextField()
    amenities = models.CharField(max_length=500, blank=True, null=True)  # comma-separated string
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_amenities_list(self):
        """Return amenities as a list for API responses."""
        if self.amenities:
            return [x.strip() for x in self.amenities.split(',')]
        return []

    def __str__(self):
        return self.name



class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField('image')
    

    def __str__(self):
        return f"{self.hotel.name}"

        
        
        
class Room(models.Model):
    ROOM_TYPES = [
        ("single", "Single"),
        ("double", "Double"),
        ("suite", "Suite"),
        ("family", "Family"),
        ("deluxe", "Deluxe"),
    ]

    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="rooms"
    )
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=2, help_text="Number of guests this room can hold")
    total_rooms = models.PositiveIntegerField(default=1, help_text="Total rooms of this type in the hotel")
    available_rooms = models.PositiveIntegerField(default=1, help_text="Rooms currently available for booking")
    is_available = models.BooleanField(default=True)  # quick flag for availability
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.get_room_type_display()}"

    class Meta:
        ordering = ["hotel", "room_type"]
