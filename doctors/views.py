from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from appointments.serializers import AppointmentSerializer
from .tokens import create_jwt_token_pair

from .models import Doctor
from .serializers import DoctorSerializer

class UserList(APIView):
    """
    List all Users and Register new user
    """

    # permission_classes = [IsAdminUser]

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

class LoginDoctor(APIView):
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


# not yet tested
class LogoutDoctor(APIView):
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


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        # you ill notice I have not used user=request.user since user is the CustomUser we got so we have to add doctor to specifically inform tthat the user is a doctor
        user = request.user.doctor
        serializer = DoctorSerializer(user, many=False)
        return Response(serializer.data)
    
# not tested
class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user.doctor
        data = request.data
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.email = data.get('email')
        user.password = data.get('password')
        user.phone_number = data.get('phone_number')
        user.date_of_birth = data.get('date_of_birth')
        user.gender = data.get('gender')
        user.bio = data.get('bio')
        user.specialization = data.get('specialization')
        user.years_of_experience = data.get('years_of_experience')
        user.clinic = data.get('clinic')
        user.time_slot = data.get('time_slot')
        user.address = data.get('address')
        if user.password:
            user.set_password(user.password) 

        user.save()

        serializer = DoctorSerializer(user, many=False)
        try:
            response = {
                    "message": "Doctor details updated successfully",
                    "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class ViewAppointments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user.id
        doctor = Doctor.objects.get(id=user)
        appointments = doctor.clinic_appointments.filter(appointment_status='BOOKED')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)