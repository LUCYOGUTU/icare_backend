from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views


urlpatterns = [
    path('token/obtain_pair', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', views.UserList.as_view(), name='user_list'),
    path('login-user/', views.UserLogin.as_view(), name='login-user'),
]

    # "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3Nzc0OTA5MiwiaWF0IjoxNjc3NjYyNjkyLCJqdGkiOiI0NTdiZTJmYzFlNjA0MTVlOTIyZjY5YTc0ZWNjYmU5MSIsInVzZXJfaWQiOjF9.3CU4kceC1Ba1OLG_xj8taStAAid0qNctFGqP2ZdKepU",
    # "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgyODQ2NjkyLCJpYXQiOjE2Nzc2NjI2OTIsImp0aSI6IjgxZGFkYjg5MDBmNTQwNGI5OTRkNWFkMDZlMDZkMmEzIiwidXNlcl9pZCI6MX0.FyOEN5j_NBFzRL7GhQibl23fHFz4H7ERJ2JexpUdxco"