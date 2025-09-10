from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,AllowAny
from users.serializers import UserSerializer,ContactSerializer
# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()
from users.models import Contact
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    # Custom permissions
    def get_permissions(self):
        """
        Allow anyone to create a contact (submit form),
        but only admins can list, retrieve, update, or delete contacts.
        """
        if self.action == "create":
            return [AllowAny()]
        return [IsAdminUser()]
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print("Contact creation error:", e)  # this prints the real error in console
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)