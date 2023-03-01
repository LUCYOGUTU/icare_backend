from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import CustomUser
from .serializers import CustomUserSerializer
from .tokens import create_jwt_token_pair

class UserList(APIView):
    """
    List all Users and create/register user
    """
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    

class RegisterPatient(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request)

            response = {
                "message": "User patient created successfully",
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