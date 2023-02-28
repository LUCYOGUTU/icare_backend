from rest_framework import serializers

from .models import Doctor, Availability
from patients.models import GENDER_CHOICES

class DoctorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    phone_number = serializers.IntegerField()
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'email', 'password', 'phone_number', 'date_of_birth', 'gender', 'bio', 'specialization', 'years_of_experience', 'clinic', 'time_slot', 'address')



# data given
# {
#     "first_name": "George",
#     "last_name": "Hewer",
#     "email": "george@gmail.com",
#     "password": "lucy@2000!",
#     "phone_number": 796101125,
#     "date_of_birth": "2023-01-14",
#     "gender": "F",
#     "bio": "Doctor",
#     "specialization": "Dentist",
#     "years_of_experience": 5,
#     "clinic": "Denti-Doc",
#     "time_slot":30,
#     "address": "Mwembe"
# }


# response (you might notice the change in time slot)
# {
#     "first_name": "George",
#     "last_name": "Hewer",
#     "email": "george@gmail.com",
#     "password": "lucy@2000!",
#     "phone_number": 796101125,
#     "date_of_birth": "2023-01-14",
#     "gender": "F",
#     "bio": "Doctor",
#     "specialization": "Dentist",
#     "years_of_experience": 5,
#     "clinic": "Denti-Doc",
#     "time_slot": "00:00:30", 
#     "address": "Mwembe"
# }



class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = '__all__'