from datetime import datetime, timedelta
import re
import hashlib
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt import views as simplejwt_views, serializers as simplejwt_serializers
from authentication.exceptions import VerificationCodeSendingFailed
from authentication.helpers import hash_code
from authentication.models import OTP
from authentication.token import TwoFAToken
from handonvitals.settings import DEFAULT_CHARSET, HASH_SALT, OTP_TIME


class CodeSendingFailed(Exception):
    pass


def send_verification_code_via_email(user, code):
    user_email_address = getattr(user, 'email', None)
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, user_email_address):
        raise CodeSendingFailed(_("No e-mail address known"))

    subject_template = _("{code}: Your verification code")
    body_template = _("{code} is the verification code needed for the login. You have {time} minutes to input it.")

    messages_sent = send_mail(
        subject=subject_template.format(code=code),
        message=body_template.format(code=code, time=settings.OTP_TIME//60),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email_address],
        fail_silently=True)

    if not messages_sent:
        raise CodeSendingFailed(_("Unable to send e-mail"))


def generate_and_send_code(user):
    code = str(randint(100000, 999999)) # generates 6-digit number
        
    try:
        send_verification_code_via_email(user, code)
    except CodeSendingFailed as error:
        raise VerificationCodeSendingFailed(error)

    code_hash = hash_code(code)
    validity = datetime.now() + timedelta(minutes=OTP_TIME)
    
    # Delete any previous OTP codes for the user
    OTP.objects.filter(user=user).delete()
    OTP.objects.create(user=user, code_hash=code_hash, validity=validity)


class CodeObtainSerializer(simplejwt_serializers.TokenObtainSerializer):
    token_class = TwoFAToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data["2fa_access"] = str(refresh)

        generate_and_send_code(self.user)

        return data


class TwoFAuthenticationView(simplejwt_views.TokenObtainPairView):
    """
    POST /auth/2fa 
    Expects "email" and "password" in body
    If user exists, returns 2fa jwt token (that only works in POST /auth/token)
    And sends email to the user with a OTP code
    """
    serializer_class = CodeObtainSerializer
