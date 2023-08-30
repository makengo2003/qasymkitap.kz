from django.db import models


choices = (("kz", "Қазақ әдебиеті"), ("world", "Әлем әдебиеті"), ("children", "Балалар әдебиеті"))


class Product(models.Model):
    category = models.CharField(max_length=50, choices=choices)
    name = models.CharField(max_length=100)
    name_lower = models.CharField(max_length=500, null=True, editable=False, blank=True)
    poster = models.ImageField(upload_to="posters/")
    price = models.PositiveIntegerField()
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.name_lower = self.name.lower() if self.name else None
        return super().save(*args, **kwargs)


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
