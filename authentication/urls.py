from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.send import TwoFAuthenticationView
from authentication.receive import TwoFAuthenticationConfirmView

urlpatterns = [
    path('2fa/', TwoFAuthenticationView.as_view(), name='token_obtain_2fa'),
    path('token/', TwoFAuthenticationConfirmView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
