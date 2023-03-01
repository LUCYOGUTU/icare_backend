from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import CustomUser, Review, GENDER_CHOICES


class CustomUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number', 'date_of_birth', 'gender')

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'gender': self.validated_data.get('gender'),
            'date_of_birth': self.validated_data.get('date_of_birth'),
        }

    # override save method
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.password1 = self.cleaned_data.get('password')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.gender = self.cleaned_data.get('gender')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.save()
        Token.objects.create(user=user)
        adapter.save_user(request, user, self)
        
        return user


# data given
# {
#     "first_name": "Janet",
#     "last_name": "Weber",
#     "email": "janet@gmail.com",
#     "password1": "xv@2000!",
#     "password2": "xv@2000!",
#     "phone_number": 796101125,
#     "date_of_birth": "2023-01-14",
#     "gender": "F"
# }

# response
# {
#     "id": 4,
#     "first_name": "Janet",
#     "last_name": "Weber",
#     "email": "janet@gmail.com",
#     "phone_number": 796101125,
#     "date_of_birth": "2023-01-14",
#     "gender": "F"
# }


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'