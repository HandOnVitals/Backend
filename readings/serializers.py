from rest_framework import serializers
from readings.models import Reading, ScoreSystemReading

class ScoreSystemReadingSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='score_system.name')
    spec = serializers.ReadOnlyField(source='score_system.spec')

    class Meta:
        model = ScoreSystemReading
        fields = ['name', 'spec', 'value']


class ReadingSerializer(serializers.ModelSerializer):
    scores = ScoreSystemReadingSerializer(source='scoresystemreading_set', many=True, read_only=True)
    # Datetime must be previous than current date
    class Meta:
        model = Reading
        fields = ['datetime', 'temperature', 'heart_rate', 'respiratory_rate', 'blood_oxygen', 'blood_pressure', 'scores']