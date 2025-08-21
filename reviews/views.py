from rest_framework.viewsets import ModelViewSet
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_pk")  # nested route
        return Review.objects.filter(hotel_id=hotel_id)

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get("hotel_pk")  # get hotel from URL
        serializer.save(user=self.request.user, hotel_id=hotel_id)
