from rest_framework import serializers
from .models import Request


class RequestSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField("get_created_at")

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d.%m.%Y, %H:%M")

    class Meta:
        model = Request
        fields = "__all__"

    def create(self, validated_data):
        return Request.objects.create(**validated_data)
