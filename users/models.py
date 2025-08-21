from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from users.managers import CustomUserManager  # pyright: ignore[reportMissingImports]
from cloudinary.models import CloudinaryField


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Optional fields
    profile_picture = CloudinaryField('image')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)

    # Admin flags
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Fix for groups and permissions clash
    groups = models.ManyToManyField(
        Group,
        related_name="custom_users",  
        blank=True,
        help_text="The groups this user belongs to."
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_users",  
        blank=True,
        help_text="Specific permissions for this user."
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
