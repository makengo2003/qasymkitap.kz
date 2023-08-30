from django.urls import path
from .views import *

urlpatterns = [
    path("", main_page_view),
    path("search/", search_page_view),
    path("wishlist/", wishlist_page_view),
    path("book_cards/", book_cards_view),
    path("category/", category_page_view),
    path("cart/", cart_page_view),
    path("book/<int:book_id>/", book_page_view),
    path("admin/", admin_page_view)
]