from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from .models import CustomUser, Review
from .serializers import CustomUserSerializer, ReviewSerializer

class UserList(APIView):
    """
    List all Users
    """
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)