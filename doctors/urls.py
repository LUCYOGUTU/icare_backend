from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('register-user/', views.RegisterDoctor.as_view(), name='register-user'),
    path('login-user/', views.UserLogin.as_view(), name='login-user'),

]