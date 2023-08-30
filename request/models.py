from django.db import models

from project.utils import datetime_now


class Request(models.Model):
    category = models.CharField(max_length=50, choices=(("books", "BOOKS"), ("languages", "LANGUAGES"), ("certificates", "CERTIFICATES")))
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=datetime_now, editable=False)
    is_accepted = models.BooleanField(default=False)
    request_text = models.TextField(default="", blank=True)
