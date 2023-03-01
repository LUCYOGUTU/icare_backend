from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .tokens import create_jwt_token_pair

from .models import Doctor
from .serializers import DoctorSerializer

class UserList(APIView):
    """
    List all Users and Register new user
    """

    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        users = Doctor.objects.all()
        serializer = DoctorSerializer(users, many=True)
        return Response(serializer.data)


class RegisterDoctor(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "User doctor created successfully",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class UserLogin(APIView):
    """
    Login Users
    """
    def get(self, request, format=None):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        # data posted
        # {
        #     "email": "george@gmail.com",
        #     "password": "xv@2000!"
        # }

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_token_pair(user)
            response = {
                "message": "Login Successful",
                "tokens": tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": "Invalid email or password",
            }
            return Response(data=response)
