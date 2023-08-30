from django.db import models


CONTACT_TYPES = (
    ("phone_number", "Номер телефона"),
    ("whatsapp", "Whatsapp"),
    ("email", "Эл. почта"),
    ("instagram", "Instagram"),
    ("footer", "Footer"),
)


class Contact(models.Model):
    contact = models.CharField(max_length=500)
    link = models.CharField(max_length=500, default="")
    type = models.CharField(max_length=100, choices=CONTACT_TYPES, unique=True)


class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel_images/")
    link = models.CharField(max_length=500, default="/")

    def __str__(self):
        return f"{self.link} ... {self.image.url}"
