from rest_framework import serializers
import random
from django.conf import settings
from datetime import datetime, timedelta
from .models import User
from .utils import send_otp

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={"min_length": f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters."}
    )

    password2 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={"min_length": f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters."}
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        otp = random.randint(100000, 999999)
        otp_exp = datetime.now() + timedelta(minutes=10)

        user = User(
            email=validated_data["email"],
            otp=otp,
            otp_exp=otp_exp,
            max_otp_try=settings.MAX_OTP_TRY,
        )
        user.set_password(validated_data["password1"])
        send_otp(email=validated_data["email"], otp=otp )
        user.save()
        return user
