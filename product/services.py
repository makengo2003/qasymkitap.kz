import functools
import os
from typing import Optional, Mapping, Union

from django.db.models import Q
from django.shortcuts import get_object_or_404

from project import settings
from .models import Product
from .serializers import ProductSerializer, ProductFormSerializer, ProductsSerializer


def get_products(products_filtration: Optional[Mapping] = None, order_by: Optional[str] = "-id", serialize: Optional[bool] = True) \
        -> Union[ProductsSerializer, Mapping]:
    products_filtration = {} if not products_filtration else products_filtration
    products = Product.objects.filter(**products_filtration).defer("description").order_by(order_by).values()
    serializer = ProductsSerializer(products, many=True)

    return serializer if serialize else serializer.data


def get_product(product_id: int, serialize: Optional[bool] = True) -> Union[ProductSerializer, Mapping]:
    product = Product.objects.filter(id=product_id).prefetch_related("options").first()
    serializer = ProductSerializer(product)

    return serializer if serialize else serializer.data


def delete_product(product_id: int) -> None:
    Product.objects.filter(id=product_id).delete()


def add_product(data: Mapping, files: Mapping) -> None:
    serializer = ProductFormSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(files=files)


def edit_product(product_id: int, data: Mapping, files: Mapping) -> None:
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductFormSerializer(product, data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(files=files)


def search_books(search_input, serialize=True):
    words = search_input.split()
    icontains_filters = [Q(name_lower__icontains=query.lower()) | Q(author_lower__icontains=query.lower()) for query in words]
    combined_filter = functools.reduce(lambda a, b: a | b, icontains_filters)
    products = Product.objects.filter(combined_filter).defer("description").order_by("-id").values()
    serializer = ProductsSerializer(products, many=True)

    return serializer if serialize else serializer.data
