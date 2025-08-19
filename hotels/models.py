from django.db import models
from django.utils.text import slugify
# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    description = models.TextField()
    stars = models.IntegerField(default=3)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.JSONField(default=list, blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    available_rooms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="hotels/")
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.name} Image"
    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    room_type = models.CharField(max_length=50)  # Single, Double, Suite
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_type} - {self.hotel.name}"
