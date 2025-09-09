from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from users.serializers import UserSerializer
# Create your views here.
from django.contrib.auth import get_user_model
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]