from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
from .models import CustomUser
from .serializers import CustomUserSerializer
from .tokens import create_jwt_token_pair

class UserList(APIView):
    """
    List all Users(patients and doctors)
    """
    # permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    

class RegisterPatient(APIView):
    """
    Register Patients
    """
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


class LoginPatient(APIView):
    """
    Login Patients
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
        

# not yet tested
class LogoutPatient(APIView):
    """
    Logout Patients
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response(data=e, status=status.HTTP_400_BAD_REQUEST)
        

# forgot password/ reset view should go here


class DoctorList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        users = Doctor.objects.all()
        serializer = DoctorSerializer(users, many=True)
        return Response(serializer.data)
    

class DoctorDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,  pk, format=None):
        users = Doctor.objects.get(id=pk)
        serializer = DoctorSerializer(users, many=False)
        return Response(serializer.data)
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        serializer = CustomUserSerializer(user, many=False)
        return Response(serializer.data)
    
# not working (work in progress)
class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user.customuser
        serializer = CustomUserSerializer(user, many=False)
        if serializer.is_valid():
            serializer.save(request)

            response = {
                "message": "Patient details updated successfully",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    