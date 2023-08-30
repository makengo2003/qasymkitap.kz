from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login

from rest_framework.request import Request

from typing import Mapping
from .serializers import ChangePasswordSerializer


def change_password(request: Request, user: User, data: Mapping) -> None:
    serializer = ChangePasswordSerializer(user, data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    auth_login(request, user)


def login(request, data):
    form = AuthenticationForm(request, data)

    if form.is_valid():
        user = form.get_user()
        auth_login(request, user)
        return True
    return False
