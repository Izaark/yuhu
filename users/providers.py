from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def create_user_by_credentials(username: str, email: str, password: str) -> User:
    return User.objects.create_user(username, email, password)


def get_or_create_token_by_user(user: User) -> Token:
    token, _ = Token.objects.get_or_create(user=user)
    return token
