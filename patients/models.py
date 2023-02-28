from django.contrib.auth.models import AbstractUser
# from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# from doctors.models import Doctor
from .managers import CustomUserManager


GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.IntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        details = self.first_name + " " + self.last_name + " " + self.email
        return details


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hcw = models.ForeignKey("doctors.Doctor", related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
