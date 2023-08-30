from django.urls import path
from .views import *


urlpatterns = [
    path("get_languages/", get_languages_view, name="get_languages"),
    path("save_languages/", save_languages_view, name="save_languages"),
    path("get_base_site_settings/", get_base_site_settings_view, name="get_base_site_settings"),
    path("save_base_site_settings/", save_base_site_settings_view, name="save_base_site_settings"),
    path("get_carousel_images/", get_carousel_images_view, name="get_carousel_images"),
    path("save_carousel_images/", save_carousel_images_view, name="save_carousel_images"),
]
