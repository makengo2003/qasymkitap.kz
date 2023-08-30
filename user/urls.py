from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *


urlpatterns = [
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change_password/", change_password_view, name="change_password"),
]
