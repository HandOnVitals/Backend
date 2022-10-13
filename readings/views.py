from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from readings.models import Reading
from readings.serializers import ReadingSerializer

class Readings(APIView):
    """
    POST /readings
    Create a new reading
    """
    def post(self, request, format=None):
        serializer = ReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReadingsObject(APIView):
    def get_object(self, pk):
        return get_object_or_404(Reading, pk=pk)

    """
    GET /readings/<reading_id>
    Get a reading
    """
    def get(self, request, reading_id, format=None):
        reading = self.get_object(reading_id)
        serializer = ReadingSerializer(reading)
        return Response(serializer.data)

    """
    PUT /readings/<reading_id>
    Update a reading
    """
    def put(self, request, reading_id, format=None):
        reading = self.get_object(reading_id)
        serializer = ReadingSerializer(reading, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    DELETE /readings/<reading_id>
    Delete a reading
    """
    def delete(self, request, pk, format=None):
        reading = self.get_object(pk)
        reading.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
