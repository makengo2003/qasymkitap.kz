import json

from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template.loader import render_to_string

from project.utils import request_schema_validation
from user import services
from product import services as product_services, schemas
from site_settings import services as site_settings_services


def main_page_view(request):
    carousel_imgs = site_settings_services.get_carousel_images(serialize=False)
    books = product_services.get_products(serialize=False)[:5]
    languages = site_settings_services.get_languages()
    render_languages = []

    for language in languages:
        render_languages.append(languages[language])

    return render(request, "main_page.html", {"books": books, "carousel_imgs": carousel_imgs, "languages": render_languages})


def search_page_view(request):
    books = product_services.search_books(request.GET.get("search_input"), serialize=False)
    return render(request, "search_page.html", {"books": books})


def wishlist_page_view(request):
    return render(request, "wishlist_page.html")


@api_view(["GET"])
@request_schema_validation("GET", schemas.GetProductsRequestSchema)
def book_cards_view(request):
    products_filtration = request.query_params.get("products_filtration", {})
    order_by = request.query_params.get("order_by", "-id")

    books = product_services.get_products(products_filtration, order_by=order_by, serialize=False)
    serialized_content = json.dumps({'html': render_to_string("book_cards.html", {"books": books})})

    return Response(serialized_content)


def category_page_view(request):
    return render(request, "category_page.html")


def cart_page_view(request):
    return render(request, "cart_page.html")


def book_page_view(request, book_id):
    book = product_services.get_product(book_id, serialize=False)
    books = product_services.get_products({"category": book["category"]}, serialize=False)[:5]
    return render(request, "book_page.html", {"books": books, "book": book})


def admin_page_view(request):
    if request.method == "POST":
        logged_in = services.login(request, request.POST)
        if logged_in:
            return redirect("/admin/")

    if request.user.is_authenticated:
        return render(request, "admin_page.html")

    return render(request, "login_page.html")
