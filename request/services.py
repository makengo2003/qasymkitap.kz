from datetime import datetime
from threading import Thread

import requests

from typing import Mapping, MutableMapping

from django.db.models import Case, When, Value, BooleanField, Sum

from product.models import Product
from project.settings import BOT_TOKEN
from project.utils import datetime_now
from site_settings import services as site_settings_services
from .serializers import RequestSerializer
from .models import Request


def send_tg_messages(text):
    tg_ids = site_settings_services.get_tg_ids()

    for tg_id in tg_ids:
        response = requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
            data={
                'chat_id': tg_id,
                'text': text,
                'parse_mode': 'html'
            }
        )
        print(response.status_code, response.json())


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
    text = (f"<b>Номер заказа №{request.id}\n</b>"
            f"<b>Тип:</b> {request.get_category_display()}\n"
            f"<b>ФИО:</b> {request.fullname}\n",
            f"<b>Номер телефона:</b> {request.phone_number}\n"
            f"<b>Время:</b> {request.created_at}\n")
    text = "\n".join(text)

    if request.category == "languages":
        text += f"<b>Тіл:</b> {request.request_text}"
    elif request.category == "books":
        cart_text = request.request_text.replace("<li>", "").replace("</li>", "\n")
        text += f'\n<b>Себетте:</b>\n{cart_text}'

    Thread(daemon=True, target=send_tg_messages, args=(text,)).start()


def get_requests(category) -> RequestSerializer:
    requests_objs = Request.objects.filter(category=category).order_by("-created_at")
    return RequestSerializer(requests_objs, many=True)


def accept_request(request_id: int) -> str:
    dt_now = datetime_now()
    Request.objects.filter(id=request_id).update(is_accepted=True, accepted_at=dt_now)
    return dt_now.strftime("%d.%m.%Y, %H:%M")


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
