from rest_framework_simplejwt import serializers as simplejwt_serializers

class TokenRefreshSerializer(simplejwt_serializers.TokenRefreshSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.get_full_name()

        return token