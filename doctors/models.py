from django.conf import settings
from django.db import models
class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
        return self.user.first_name + " " + self.user.last_name


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

