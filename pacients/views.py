from rest_framework.views import APIView
from readings.models import Reading
from pacients.models import Pacient
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from readings.serializers import ReadingSerializer

class PacientData(APIView):
    def get_object(self, pacient_health_number):
        # import time
        # time.sleep(20)
        return get_object_or_404(Pacient, health_number=pacient_health_number)

    def get(self, request, pacient_health_number, format=None):
        pacient = self.get_object(pacient_health_number)
        # Get the readings cronologically ordered (from most recent to oldest)
        readings = Reading.objects.filter(pacient=pacient).order_by('-datetime')
        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)
