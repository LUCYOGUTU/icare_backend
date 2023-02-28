from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from .models import Doctor, Availability
from .serializers import DoctorSerializer, AvailabilitySerializer

class UserList(APIView):
    """
    List all Users
    """
    def get(self, request, format=None):
        users = Doctor.objects.all()
        serializer = DoctorSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
