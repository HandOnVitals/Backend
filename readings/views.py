from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from readings.models import Reading
from readings.serializers import ReadingSerializer

class ReadingList(APIView):
    """
    List all readings, or create a new reading.
    """
    def get(self, request, format=None):
        readings = Reading.objects.all()
        serializer = ReadingSerializer(readings, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReadingDetail(APIView):
    """
    Retrieve, update or delete a reading instance.
    """
    def get_object(self, pk):
        return get_object_or_404(Reading, pk=pk)

    def get(self, request, pk, format=None):
        reading = self.get_object(pk)
        serializer = ReadingSerializer(reading)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        reading = self.get_object(pk)
        serializer = ReadingSerializer(reading, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        reading = self.get_object(pk)
        reading.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)