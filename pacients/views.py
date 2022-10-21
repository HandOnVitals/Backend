from rest_framework.views import APIView
from readings.models import Reading
from pacients.models import Pacient
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from readings.serializers import ReadingSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class Pacients(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, health_number: str):
        # import time
        # time.sleep(20)
        return get_object_or_404(Pacient, health_number=health_number)

    """
    GET /pacients/<health_number>/readings
    Retrieve all readings for pacient <health_number>
    """
    def get(self, request, health_number: str, format=None):
        self.pacient = self.get_object(health_number)
        # Get the readings cronologically ordered (from most recent to oldest)
        readings = Reading.objects.filter(pacient=self.pacient).order_by('-datetime')
        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)

    """
    POST /pacients/<health_number>/readings
    Create a reading for pacient <health_number>
    """
    def post(self, request, health_number: str, format=None):
        try:
            self.pacient = Pacient.objects.get(health_number=health_number)
        except Pacient.DoesNotExist:
            self.pacient = Pacient.objects.create(health_number=health_number)

        serializer = ReadingSerializer(data=request.data)
        if serializer.is_valid():
            if Reading.objects.filter(pacient=self.pacient, datetime=serializer.validated_data['datetime']).exists():
                return Response({'error': 'A reading with that <pacient,date> combination already exists'}, status=status.HTTP_409_CONFLICT)
            
            serializer.validated_data['pacient'] = self.pacient
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
