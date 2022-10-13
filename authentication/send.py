import re
import pyotp
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt import views as simplejwt_views, serializers as simplejwt_serializers
from authentication.exceptions import VerificationCodeSendingFailed
from authentication.token import TwoFAToken


class CodeSendingFailed(Exception):
    pass


def send_verification_code_via_email(user, code):
    user_email_address = getattr(user, 'email', None)
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, user_email_address):
        raise CodeSendingFailed(_("No e-mail address known"))

    subject_template = _("{code}: Your verification code")
    body_template = _("{code} is the verification code needed for the login.")

    messages_sent = send_mail(
        subject=subject_template.format(code=code),
        message=body_template.format(code=code),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email_address],
        fail_silently=True)

    if not messages_sent:
        raise CodeSendingFailed(_("Unable to send e-mail"))


class CodeObtainSerializer(simplejwt_serializers.TokenObtainSerializer):
    token_class = TwoFAToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data["2fa_access"] = str(refresh)

        totp = pyotp.TOTP(settings.OTP_KEY, interval=settings.OTP_TIME)
        code = totp.now()
        
        try:
            send_verification_code_via_email(self.user, code)
        except CodeSendingFailed as error:
            raise VerificationCodeSendingFailed(error)

        return data


class TwoFAuthenticationView(simplejwt_views.TokenObtainPairView):
    """
    POST /auth/2fa 
    Expects "email" and "password" in body
    If user exists, returns 2fa jwt token (that only works in POST /auth/token)
    And sends email to the user with a OTP code
    """
    serializer_class = CodeObtainSerializer
