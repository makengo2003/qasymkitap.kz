from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.request import Request

from project.utils import request_schema_validation
from . import services, schemas


@api_view(["GET"])
@request_schema_validation("GET", schemas.GetProductsRequestSchema)
def get_products_view(request: Request) -> Response:
    serialized_products = services.get_products(request.query_params.get("products_filtration", {}))
    return Response(serialized_products.data)


@api_view(["GET"])
@request_schema_validation("GET", schemas.ProductIdSchema)
def get_product_view(request: Request) -> Response:
    serialized_product = services.get_product(request.query_params.get("product_id"))
    return Response(serialized_product.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def add_product_view(request: Request) -> Response:
    services.add_product(request.data, request.FILES)
    return Response({"success": True})


@api_view(["POST"])
@permission_classes([IsAdminUser])
@request_schema_validation("POST", schemas.ProductIdSchema)
def delete_product_view(request: Request) -> Response:
    services.delete_product(request.data.pop("product_id"))
    return Response({"success": True})


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def edit_product_view(request: Request) -> Response:
    services.edit_product(request.data.get("id"), request.data, request.FILES)
    return Response({"success": True})
