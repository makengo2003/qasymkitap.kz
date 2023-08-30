import requests

from typing import Mapping, MutableMapping

from django.db.models import Case, When, Value, BooleanField, Sum

from product.models import Product
from project.settings import BOT_TOKEN
from site_settings import services as site_settings_services
from .serializers import RequestSerializer
from .models import Request


def leave_request(data: MutableMapping) -> None:
    cart_items = data.pop("cart_items", False)

    serializer = RequestSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    if cart_items:
        request_text = ""
        total_price = 0

        product_ids = []
        for cart_item in cart_items:
            request_text += f"<li>{cart_item['count']} шт {cart_item['book_name']}</li>\n"
            product_ids.append(cart_item["book_id"])

        prices = Product.objects.filter(id__in=product_ids).values_list("price", flat=True)
        for i in range(len(prices)):
            total_price += prices[i] * int(cart_items[i]["count"])

        request_text += f"<li>Барлығы: {total_price} тг</li>"

        serializer.validated_data["request_text"] = request_text

    request = serializer.save()

    # contacts = site_settings_services.get_contacts()
    # email = None
    #
    # for contact in contacts.data:
    #     if contact["type"] == "email":
    #         email = contact["contact"]
    #         break
    #
    # requests.post(
    #     f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
    #     data={
    #         'chat_id': email,
    #         'text': request.request_text,
    #         'parse_mode': 'html'
    #     }
    # )


def get_requests(category) -> RequestSerializer:
    requests_objs = Request.objects.filter(category=category).order_by("-created_at")
    return RequestSerializer(requests_objs, many=True)


def accept_request(request_id: int) -> None:
    Request.objects.filter(id=request_id).update(is_accepted=True)


def check_new_requests():
    new_requests = Request.objects.annotate(
        books=Case(
            When(is_accepted=False, category="books", then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
        languages=Case(
            When(is_accepted=False, category="languages", then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
        certificates=Case(
            When(is_accepted=False, category="certificates", then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
    ).all().values("books", "languages", "certificates")[0]

    print(new_requests)

    return {
        "books": new_requests["books"],
        "languages": new_requests["languages"],
        "certificates": new_requests["certificates"]
    }
