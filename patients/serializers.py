from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from allauth.utils import email_address_exists

from .models import CustomUser, Review, GENDER_CHOICES


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    phone_number = serializers.IntegerField()
    date_of_birth = serializers.DateField()
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'phone_number', 'date_of_birth', 'gender')

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

    # override save method of RegisterSerializer
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
        adapter.save_user(request, user, self)
        return user


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'