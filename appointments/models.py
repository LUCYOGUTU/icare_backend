from django.db import models

from doctors.models import Doctor
from patients.models import CustomUser

class Appointment(models.Model):
    STATUS = (
        ('ACTIVE', 'Active'),
        ('CANCELED', 'Canceled'),
        ('COMPLETE', 'Complete'),
    )

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    clinic = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='clinic_appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    appointment_status = models.CharField(max_length=10, choices=STATUS)

