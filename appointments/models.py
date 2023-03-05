from django.db import models

from doctors.models import Doctor
from patients.models import CustomUser

class Appointment(models.Model):
    STATUS = (
        ('ACTIVE', 'Active'),
        ('CANCELED', 'Canceled'),
        ('COMPLETE', 'Complete'),
        ('BOOKED', 'Booked'),
    )

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='clinic_appointments')
    date = models.DateField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    appointment_status = models.CharField(max_length=10, choices=STATUS)

    class Meta:
        verbose_name_plural = 'Appointments'

    def __str__(self):
        return f"{self.user}'s appointment with Dr. {self.doctor.name} on {self.date} at {self.start_time}"

