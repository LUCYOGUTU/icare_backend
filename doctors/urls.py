from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('register-patient/', views.RegisterDoctor.as_view(), name='register-patient'),
    path('login-patient/', views.LoginDoctor.as_view(), name='login-patient'),
    path('logout-patient/', views.LogoutDoctor.as_view(), name='logout-patient'),
    path('profile-view/', views.ProfileView.as_view(), name='profile-view'),
    path('edit-profile-view/', views.EditProfileView.as_view(), name='edit-profile-view'),

]