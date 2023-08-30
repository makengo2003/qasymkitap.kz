from django.urls import path
from . import views


urlpatterns = [
    path("leave_request/", views.leave_request_view, name="leave_request"),
    path("get_requests/", views.get_requests_view, name="get_requests"),
    path("accept_request/<int:request_id>/", views.accept_request_view, name="accept_request"),
    path("check_new_requests/", views.check_new_requests, name="check_new_requests")
]
