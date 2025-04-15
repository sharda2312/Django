import datetime
import random

from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from Account.utils import send_otp

from .models import User
from .serialiser import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    UserModel View.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["PATCH"])
    def verify_otp(self, request, pk=None):
        instance = self.get_object()
        if (
            not instance.is_active
            and instance.otp == request.data.get("otp")
            and instance.otp_exp
            and timezone.now() < instance.otp_exp
        ):
            instance.is_active = True
            instance.otp_exp = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.otp_locked_until = None
            instance.save()
            return Response(
                "Successfully verified the user.", status=status.HTTP_200_OK
            )

        return Response(
            "User active or Please enter the correct OTP.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["PATCH"])
    def regenerate_otp(self, request, pk=None):
        """
        Regenerate OTP for the given user and send it to the user.
        """
        instance = self.get_object()
        if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_locked_until:
            return Response(
                "Max OTP try reached, try after an hour",
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp = random.randint(100000, 999999)
        otp_exp = timezone.now() + datetime.timedelta(minutes=10)
        max_otp_try = int(instance.max_otp_try) - 1

        instance.otp = otp
        instance.otp_exp = otp_exp
        instance.max_otp_try = max_otp_try
        if max_otp_try == 0:
            # Set cool down time
            otp_locked_until = timezone.now() + datetime.timedelta(hours=1)
            instance.otp_locked_until = otp_locked_until
        elif max_otp_try == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY
        else:
            instance.otp_locked_until = None
            instance.max_otp_try = max_otp_try
        instance.save()
        send_otp(instance.email, otp)
        return Response("Successfully generate new OTP.", status=status.HTTP_200_OK)    