from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('__all__')

        def create(self, validated_data):
            validated_data['patient'] = self.context['request'].user
            validated_data['appointment_status'] = 'BOOKED' # Set the default status to 'booked'
            appointment = Appointment.objects.create(**validated_data)
            return appointment

        def update(self, instance, validated_data):
            instance.doctor = validated_data.get('doctor', instance.doctor)
            instance.date = validated_data.get('date', instance.date)
            instance.start_time = validated_data.get('start_time', instance.start_time)
            instance.end_time = validated_data.get('end_time', instance.end_time)
            instance.appointment_status = validated_data.get('appointment_status', instance.appointment_status)
            instance.save()
            return instance