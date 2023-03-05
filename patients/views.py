from datetime import datetime
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from appointments.serializers import AppointmentSerializer
from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
from .models import CustomUser, Review
from .serializers import CustomUserSerializer, ReviewSerializer
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
    

class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user
        
        data = request.data
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')
        user.password = data.get('password')
        user.phone_number = data.get('phone_number')
        user.date_of_birth = data.get('date_of_birth')
        user.gender = data.get('gender')

        if user.password:
            user.set_password(user.password)        

        user.save()

        serializer = CustomUserSerializer(user, many=False)
        try:
            response = {
                    "message": "Patient details updated successfully",
                    "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

#    user = User.objects.get(username='myusername')
# user.set_password('newpassword')
# user.save()     
# class UpdateUser(RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserSerializerAPI
#     queryset = User.objects.all()

#     def perform_update(self, serializer):
#         instance = serializer.save()
#         instance.set_password(instance.password)
#         instance.save()


class ViewAppointments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user.id
        patient = CustomUser.objects.get(id=user)
        appointments = patient.appointments.filter(appointment_status='BOOKED')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
class ViewCanceledAppointments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user.id
        patient = CustomUser.objects.get(id=user)
        appointments = patient.appointments.filter(appointment_status='CANCELED')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    