from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from patients.models import CustomUser

# CustomUser = get_user_model()
class Doctor(CustomUser):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    SPECIALIZATION = (
        ('Physician', 'Physician'),
        ('Dentist', 'Dentist'),
        ('Psychologist', 'Psychologist'),
        ('Pharmacist', 'Pharmacist'),
        ('Nurse', 'Nurse'),
        ('Dermatologist', 'Dermatologist'),
        ('Other', 'Other'),
    )
    bio = models.CharField(max_length=300)
    specialization = models.CharField(max_length=255, choices=SPECIALIZATION)
    years_of_experience = models.IntegerField()
    clinic = models.CharField(max_length=255)
    time_slot = models.DurationField()
    address = models.CharField(max_length=255)

    def __str__(self):
        if self.doctor is not None:
            return self.first_name + " " + self.last_name


class Availability(models.Model):
    DAY = (
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THUR', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
    )

    clinic = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=5, choices=DAY)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    reason_of_unavailability = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name_plural = 'Availability'

