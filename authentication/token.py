from rest_framework_simplejwt import tokens
from datetime import timedelta
from handonvitals.settings import OTP_TIME

class TwoFAToken(tokens.Token):
    token_type = "2fa"
    lifetime = timedelta(minutes=OTP_TIME)
