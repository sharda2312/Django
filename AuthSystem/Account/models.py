from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator, validate_email, MaxValueValidator, MinValueValidator
from django.utils import timezone
import datetime

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        user = self.create_user(email=email, password=password, **extra_fields)

        if not password:
            raise ValueError("Superuser must have a password.")

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[validate_email])
    name = models.CharField(max_length=100)
    
    # OTP-related fields
    otp = models.PositiveIntegerField(
        validators=[MinValueValidator(100000), MaxValueValidator(999999)],
        null=True,
        blank=True
    )
    otp_exp = models.DateTimeField(null=True, blank=True)
    max_otp_try = models.PositiveIntegerField(default=settings.MAX_OTP_TRY)
    otp_locked_until = models.DateTimeField(null=True, blank=True)

    # User permissions
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    user_registered_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email