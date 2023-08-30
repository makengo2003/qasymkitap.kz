import os
from typing import MutableMapping
from rest_framework import serializers
from .models import Product, ProductOption, choices


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        exclude = ["product"]


class ProductSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    poster = serializers.CharField(max_length=255)
    category_label = serializers.SerializerMethodField("get_category_label")

    class Meta:
        model = Product
        exclude = ["description"]

    def get_category_label(self, obj):
        for choice in choices:
            if choice[0] == obj["category"]:
                return choice[1]


class ProductFormSerializer(serializers.ModelSerializer):
    poster = serializers.CharField()
    options = serializers.JSONField()

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data: MutableMapping) -> Product:
        files = validated_data.pop("files", {})
        poster = files.pop(validated_data.pop("poster"))[0]
        options = validated_data.pop("options")

        product = Product(**validated_data, poster=poster)
        product.save()

        product.options.bulk_create([ProductOption(**option, product=product) for option in options])

        return product

    def update(self, product: Product, validated_data: MutableMapping) -> Product:
        files = validated_data.pop("files", {})
        poster = files.pop(validated_data.pop("poster"), False)
        options = validated_data.pop("options")

        if poster:
            product.poster.delete()
            product.poster = poster[0]
            product.save()

        Product.objects.filter(id=product.pk).update(**validated_data)
        product = Product.objects.get(id=product.pk)
        product.save()
        product.options.all().delete()
        product.options.bulk_create([ProductOption(**option, product=product) for option in options])

        return product
