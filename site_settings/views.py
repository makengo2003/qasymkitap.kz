from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from . import services


@api_view(["GET"])
def get_carousel_images_view(_):
    carousel_images = services.get_carousel_images()
    return Response(carousel_images.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def save_carousel_images_view(request):
    services.save_carousel_images(request.data, request.FILES)
    return Response({"success": True})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_languages_view(_):
    languages = services.get_languages()
    return Response(languages)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def save_languages_view(request):
    services.save_languages(request.data.get("languages", []))
    return Response({"success": True})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_tg_ids_view(_):
    tg_ids = services.get_tg_ids()
    return Response(tg_ids)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def save_tg_ids_view(request):
    services.save_tg_ids(request.data.get("tg_ids", []))
    return Response({"success": True})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_base_site_settings_view(_):
    base_site_settings = services.get_base_site_settings()
    return Response(base_site_settings)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def save_base_site_settings_view(request):
    services.save_base_site_settings(request.data)
    return Response({"success": True})
