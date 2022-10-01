from rest_framework import serializers
from pacients.models import Pacient


class PacientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacient
        fields = ['health_number']