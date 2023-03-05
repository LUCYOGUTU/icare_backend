from django.urls import path

from . import views


urlpatterns = [
    path('', views.UserList.as_view(), name='user-list'),
    path('register-patient/', views.RegisterPatient.as_view(), name='register-patient'),
    path('login-patient/', views.LoginPatient.as_view(), name='login-patient'),
    path('logout-patient/', views.LogoutPatient.as_view(), name='logout-patient'),
    path('view-doctors/', views.DoctorList.as_view(), name='view-doctors'),
    path('view-doctor/<str:pk>/', views.DoctorDetail.as_view(), name='view-doctor'),
    path('profile-view/', views.ProfileView.as_view(), name='profile-view'),
    path('edit-profile-view/', views.EditProfileView.as_view(), name='edit-profile-view'),
    path('view-appointments/', views.ViewAppointments.as_view(), name='view-appointments'),
    path('view-canceled-appointments/', views.ViewCanceledAppointments.as_view(), name='view-canceled-appointments'),
]
