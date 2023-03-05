from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('register-doctor/', views.RegisterDoctor.as_view(), name='register-doctor'),
    path('login-doctor/', views.LoginDoctor.as_view(), name='login-doctor'),
    path('logout-doctor/', views.LogoutDoctor.as_view(), name='logout-doctor'),
    path('profile-view/', views.ProfileView.as_view(), name='profile-view'),
    path('edit-profile-view/', views.EditProfileView.as_view(), name='edit-profile-view'),
    path('view-appointments/', views.ViewAppointments.as_view(), name='view-appointments'),

]