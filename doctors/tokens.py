from rest_framework_simplejwt.tokens import RefreshToken
from .models import Doctor

User = Doctor()

def create_jwt_token_pair(user:User):
    refresh = RefreshToken.for_user(user)

    tokens = {
        "access": str(refresh.access_token),
        "refresh":str(refresh)
    }
    return tokens 