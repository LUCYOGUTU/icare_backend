from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Doctor, Availability

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        # fields = ('id','first_name', 'last_name', 'email', 'password', 'phone_number', 'date_of_birth', 'gender', 'bio', 'specialization', 'years_of_experience', 'clinic', 'time_slot', 'address')
        fields = ('__all__')

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


# data given when registering a new user
# {
#     "first_name": "George",
#     "last_name": "Hewer",
#     "email": "george@gmail.com",
#     "password": "xv@2000!",
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
#     "password": "xv@2000!",
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