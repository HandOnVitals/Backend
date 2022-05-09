from rest_framework import serializers
from readings.models import Reading


class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ['datetime', 'temperature', 'heart_rate', 'respiratory_rate', 'oxygen_saturation', 'blood_pressure']