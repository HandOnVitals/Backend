from rest_framework.views import APIView
from readings.models import Reading
from pacients.models import Pacient
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from readings.serializers import ReadingSerializer
from rest_framework.permissions import IsAuthenticated


class Pacients(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, health_number: str):
        # import time
        # time.sleep(20)
        return get_object_or_404(Pacient, health_number=health_number)

    """
    GET /pacients/<health_number>/readings
    Retrieve all readings for pacient <health_number>
    """
    def get(self, request, health_number: str, format=None):
        pacient = self.get_object(health_number)
        # Get the readings cronologically ordered (from most recent to oldest)
        readings = Reading.objects.filter(pacient=pacient).order_by('-datetime')
        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)
