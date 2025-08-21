from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)  # 👈 for upload

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id', 'email', 'password',
            'first_name', 'last_name',
            'address', 'phone_number',
            'profile_picture'
        ]
        extra_kwargs = {
            'password': {'write_only': True}  # don't return password in response
        }


class UserSerializer(BaseUserSerializer):
    profile_picture = serializers.ImageField(read_only=True)  # 👈 only for display

    class Meta(BaseUserSerializer.Meta):
        ref_name = 'CustomUser'
        fields = [
            'id', 'email',
            'first_name', 'last_name',
            'address', 'phone_number',
            'profile_picture'
        ]
