from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Appointment
from .serializers import AppointmentSerializer


class BookAppointment(APIView):
    """
    Patients booking appointment with specific doctors
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data.copy()
        data['patient'] = request.user.id
        data['appointment_status'] = 'BOOKED'
        serializer = AppointmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Appointment booked successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# add the url in urls.py and test
class RescheduleAppointment(APIView):
    """
    Patients rescheduling appointment.
    """
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        try:
            appointment = Appointment.objects.get(id=pk)
            if appointment.appointment_status != 'BOOKED' or appointment.appointment_status != 'CANCELED':
                return Response({'error_detail': 'Cannot reschedule an appointment that is not booked or canceled.'}, status=status.HTTP_400_BAD_REQUEST)
            if appointment.start_time < datetime.now():
                return Response({'error_detail': 'Cannot reschedule an appointment that has already started.'}, status=status.HTTP_400_BAD_REQUEST)
            appointment.start_time = request.data['start_time']
            appointment.end_time = request.data['end_time']
            appointment.save()

            serializer = AppointmentSerializer(appointment)
            response = {
                    "message": "Appointment updated successfully",
                    "data": serializer.data
                }
            return Response(response)
        except Appointment.DoesNotExist:
            return Response({'message': 'Appointment not found.'}, status=status.HTTP_404_NOT_FOUND)

# class UpdateAppointment(APIView):
#     def put(self, request, pk):
#         appointment = Appointment.objects.get(pk=pk)
#         serializer = AppointmentSerializer(appointment, data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user, status='BOOKED')
#             response = {
#                 "message": "Appointment updated successfully",
#                 "data": serializer.data
#             }
#             return Response(response, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# add the url in urls.py
class CancelAppointment(APIView):
    """
    Patients canceling appointment.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        appointment = Appointment.objects.get(id=pk)
        appointment.appointment_status = 'CANCELED'
        appointment.save()
        return Response({'message': 'Appointment canceled'}, status=status.HTTP_200_OK)
