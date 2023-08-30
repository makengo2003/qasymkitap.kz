from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from . import services


@api_view(["POST"])
def leave_request_view(request: Request) -> Response:
    services.leave_request(request.data)
    return Response({"success": True})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_requests_view(request) -> Response:
    requests = services.get_requests(request.query_params.get("category"))
    return Response(requests.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def accept_request_view(_, request_id: int) -> Response:
    services.accept_request(request_id)
    return Response({"success": True})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def check_new_requests(request):
    response = services.check_new_requests()
    return Response(response)
