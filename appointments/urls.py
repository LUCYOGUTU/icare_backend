from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookAppointment.as_view(), name='book-appointment'),
    path('reschedule-appointment/<str:pk>/', views.RescheduleAppointment.as_view(), name='reschedule-appointmet'),
    path('cancel-appointment/<str:pk>/', views.CancelAppointment.as_view(), name='cancel-appointmet'),
]