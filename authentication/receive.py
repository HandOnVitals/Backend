from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt import authentication as simplejwt_authentication, views as simplejwt_views, tokens as simplejwt_tokens, exceptions as simplejwt_exceptions
from authentication.exceptions import VerificationCodeInvalid
from authentication.helpers import hash_code
from authentication.models import OTP
from authentication.token import TwoFAToken

class JWT2faAuthentication(simplejwt_authentication.JWTAuthentication):
    def get_validated_token(self, raw_token):
        messages = []
        try:
            return TwoFAToken(raw_token)
        except simplejwt_exceptions.TokenError as e:
            messages.append(
                {
                    "token_class": TwoFAToken.__name__,
                    "token_type": TwoFAToken.token_type,
                    "message": e.args[0],
                }
            )

        raise simplejwt_exceptions.InvalidToken(
            {
                "detail": _("Given token not valid for any token type"),
                "messages": messages,
            }
        )


def verify_code(code, user):
    code_hash = hash_code(code)

    otp_object = OTP.objects.filter(user=user, code_hash=code_hash)

    if not otp_object.exists():
        raise VerificationCodeInvalid
    
    # Get latest
    otp_object = otp_object.order_by('-validity').first()
    validity = otp_object.validity

    if datetime.now() > validity:
        raise VerificationCodeInvalid

    # Everything OK, can delete the entry from the database
    otp_object.delete()


class CodeVerifySerializer(serializers.Serializer):
    token_class = simplejwt_tokens.RefreshToken
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        try:
            req = self.context["request"]
        except KeyError:
            # Raise exception if fails
            pass
        
        # 1 - Get user and token
        user, token = JWT2faAuthentication().authenticate(req)
        
        # 2 - Verify code
        code = attrs['code']
        verify_code(code, user)
        
        # 3 - Generate new token (access and refresh)
        data = {}

        refresh = self.get_token(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        update_last_login(None, user)

        return data

    @classmethod
    def get_token(cls, user):
        token = cls.token_class.for_user(user)

        token['name'] = user.get_full_name()

        return token


class TwoFAuthenticationConfirmView(simplejwt_views.TokenObtainPairView):
    """
    POST /auth/token
    Expects "code" in body, as well as 2fa auth jwt token in Authorization header
    If both "code" and jwt token are valid
    Returns access and refresh tokens that allow users to access reserved endpoints
    """
    serializer_class = CodeVerifySerializer
