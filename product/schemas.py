from rest_framework import serializers


class ProductIdSchema(serializers.Serializer):
    product_id = serializers.IntegerField()


class GetProductsRequestSchema(serializers.Serializer):
    products_filtration = serializers.JSONField(required=False)
